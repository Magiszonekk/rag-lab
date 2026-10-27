{{- define "raglab.name" -}}raglab{{- end -}}

{{- define "raglab.fullname" -}}
{{- if contains "raglab" .Release.Name -}}{{ .Release.Name | trunc 50 | trimSuffix "-" }}
{{- else -}}{{ printf "%s-raglab" .Release.Name | trunc 50 | trimSuffix "-" }}{{- end -}}
{{- end -}}

{{- define "raglab.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
app.kubernetes.io/name: {{ include "raglab.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/* selektor komponentu: include "raglab.selector" (dict "ctx" . "component" "api") */}}
{{- define "raglab.selector" -}}
app.kubernetes.io/name: {{ include "raglab.name" .ctx }}
app.kubernetes.io/instance: {{ .ctx.Release.Name }}
app.kubernetes.io/component: {{ .component }}
{{- end -}}

{{- define "raglab.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
{{- end -}}

{{- define "raglab.secretName" -}}
{{ .Values.secrets.existingSecret | default (printf "%s-secrets" (include "raglab.fullname" .)) }}
{{- end -}}

{{- define "raglab.dbHost" -}}
{{- if .Values.postgres.enabled -}}{{ include "raglab.fullname" . }}-postgres
{{- else -}}{{ required "postgres.external.host jest wymagany, gdy postgres.enabled=false" .Values.postgres.external.host }}{{- end -}}
{{- end -}}

{{/* wspólne zmienne środowiska aplikacji (API, Joby, CronJob) */}}
{{- define "raglab.appEnv" -}}
- name: RAGLAB_DB_HOST
  value: {{ include "raglab.dbHost" . | quote }}
- name: RAGLAB_DB_PORT
  value: {{ ternary "5432" (toString .Values.postgres.external.port) .Values.postgres.enabled | quote }}
- name: RAGLAB_DB_SSLMODE
  value: {{ ternary "disable" .Values.postgres.external.sslmode .Values.postgres.enabled | quote }}
- name: POSTGRES_DB
  value: {{ .Values.postgres.database | quote }}
- name: POSTGRES_USER
  value: {{ .Values.postgres.user | quote }}
- name: POSTGRES_PASSWORD
  valueFrom: {secretKeyRef: {name: {{ include "raglab.secretName" . }}, key: POSTGRES_PASSWORD}}
- name: RAGLAB_EMBED
  value: {{ .Values.api.embed | quote }}
- name: OPENROUTER_API_KEY
  valueFrom: {secretKeyRef: {name: {{ include "raglab.secretName" . }}, key: OPENROUTER_API_KEY, optional: true}}
{{- if .Values.litellm.enabled }}
- name: RAGLAB_LITELLM_URL
  value: "http://{{ include "raglab.fullname" . }}-litellm:{{ .Values.litellm.port }}"
- name: LLM_DEMO_BASE_URL
  value: "http://{{ include "raglab.fullname" . }}-litellm:{{ .Values.litellm.port }}/v1"
- name: LLM_DEMO_MODEL
  value: demo-answer
{{- end }}
- name: LLM_DEMO_API_KEY
  valueFrom: {secretKeyRef: {name: {{ include "raglab.secretName" . }}, key: LLM_DEMO_API_KEY, optional: true}}
{{- end -}}

{{/* wolumeny wspólne: dane (PVC) + zapisywalne katalogi przy readOnlyRootFilesystem */}}
{{- define "raglab.dataMounts" -}}
- {name: data, mountPath: /data}
- {name: data, mountPath: /app/results/answers, subPath: answers}
- {name: data, mountPath: /app/results/series, subPath: series}
- {name: tmp, mountPath: /tmp}
{{- include "raglab.kvMount" . }}
{{- end -}}

{{- define "raglab.dataVolumes" -}}
- name: data
  persistentVolumeClaim: {claimName: {{ include "raglab.fullname" . }}-data}
- name: tmp
  emptyDir: {sizeLimit: 512Mi}
{{- include "raglab.kvVolume" . }}
{{- end -}}

{{/* Azure Key Vault: ServiceAccount z workload identity + wolumen CSI (synchronizuje Secret) */}}
{{- define "raglab.podIdentity" -}}
{{- if .Values.azure.keyVault.enabled }}
serviceAccountName: raglab
{{- end }}
{{- end -}}


{{- define "raglab.kvMount" -}}
{{- if .Values.azure.keyVault.enabled }}
- {name: kv, mountPath: /mnt/secrets, readOnly: true}
{{- end }}
{{- end -}}

{{- define "raglab.kvVolume" -}}
{{- if .Values.azure.keyVault.enabled }}
- name: kv
  csi:
    driver: secrets-store.csi.k8s.io
    readOnly: true
    volumeAttributes: {secretProviderClass: {{ include "raglab.fullname" . }}-kv}
{{- end }}
{{- end -}}

{{/* kontener tunelu WireGuard (wireproxy) do bramki modeli — w podzie LiteLLM i w Jobie ewaluacji */}}
{{- define "raglab.tunnelContainer" -}}
- name: tunnel
  image: {{ .Values.litellm.tunnel.image }}
  args: ["--config", "/etc/wireproxy/config", "--info", "127.0.0.1:9080"]
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities: {drop: [ALL]}
  resources: {{- toYaml .Values.litellm.tunnel.resources | nindent 4 }}
  volumeMounts:
    - {name: wg, mountPath: /etc/wireproxy, readOnly: true}
{{- end -}}

{{- define "raglab.tunnelVolume" -}}
- name: wg
  secret:
    secretName: {{ include "raglab.secretName" . }}
    items: [{key: WIREGUARD_CONF, path: config}]
    defaultMode: 0444
{{- end -}}
