# Przegląd ręczny werdyktów sędziego (golden v1)

Spory: 105, próbka zgodnych: 15.


## simple/verify=off · g-vat-08 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie urząd skarbowy powinien zwrócić podatnikowi różnicę podatku VAT (nadwyżkę podatku naliczonego nad należnym) na rachunek bankowy?
**Wzorzec:** Zwrot różnicy podatku następuje w terminie 40 dni od dnia złożenia rozliczenia przez podatnika, z zastrzeżeniem wyjątków wskazanych w ust. 6, 6a i 6d art. 87.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 87 ust. 2, VAT art. 87 ust. 6a, VAT art. 87 ust. 6 pkt 1–4, VAT art. 87 ust. 6d): Co do zasady zwrot różnicy podatku VAT na rachunek bankowy następuje w terminie 40 dni od dnia złożenia rozliczenia (VAT art. 87 ust. 2). Termin może wynosić 25 dni od dnia złożenia rozliczenia, jeżeli podatnik spełnia łącznie warunki określone w VAT art. 87 ust. 6 pkt 1–4, albo 15 dni w przypadkach określonych w VAT art. 87 ust. 6d. Na wniosek podatnika zawarty w deklaracji zwrot na rachunek VAT następuje w terminie 25 dni od dnia złożenia rozliczenia (VAT art. 87 ust. 6a), co nie dotyczy zwykłego rachunku bankowego. Jeżeli zasadność zwrotu wymaga dodatkowego zweryfikowania, termin może zostać przedłużony do czasu zakończenia weryfikacji (VAT art. 87 ust. 2).
**Kontekst:** VAT art. 87 ust. 2, VAT art. 87 ust. 6d, VAT art. 87 ust. 6a, VAT art. 87 ust. 6 pkt 1–3, VAT art. 87 ust. 6 pkt 4
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie wskazuje podstawowy termin 40 dni oraz dokładnie opisuje wyjątki (25 dni z warunkami ust.6, 15 dni z ust.6d, 25 dni na rachunek VAT z ust.6a) i możliwość przedłużenia terminu w razie weryfikacji – wszystko zgodne z przepisami w kontekście, bez błędów.
**Sędzia 2** (gpt-5.6-terra): partial — Prawidłowo wskazano zasadę 40 dni od złożenia rozliczenia oraz wyjątki. Błędnie jednak uogólniono termin 15 dni z art. 87 ust. 6d jako liczony zawsze od złożenia rozliczenia; przepis uzależnia jego początek od terminu złożenia deklaracji albo złożenia korekty.

## simple/verify=off · g-vat-13 (multi, oczekiwane: answer)
**Pytanie:** Spółka A i spółka B należą do tej samej grupy VAT. Czy sprzedaż towarów między nimi podlega opodatkowaniu VAT?
**Wzorzec:** Nie — dostawa towarów i świadczenie usług dokonane przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlegają opodatkowaniu (art. 8c ust. 1), o ile spółki A i B tworzą grupę VAT w rozumieniu art. 2 pkt 47, czyli grupę podmiotów powiązanych finansowo, ekonomicznie i organizacyjnie, zarejestrowaną jako podatnik podatku.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 8c ust. 1): Nie. Dostawa towarów dokonana przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlega opodatkowaniu VAT (VAT art. 8c ust. 1).
**Kontekst:** VAT art. 8c, VAT art. 14 ust. 9c, Ordynacja art. 86a § 6
**Sędzia 1** (claude-sonnet-5): partial — Poprawnie wskazuje art. 8c ust. 1 i brak opodatkowania, ale pomija świadczenie usług oraz warunek, że A i B muszą faktycznie tworzyć grupę VAT w rozumieniu art. 2 pkt 47 (co wzorzec zaznacza).
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje, że dostawa towarów między członkami tej samej grupy VAT nie podlega opodatkowaniu, zgodnie z art. 8c ust. 1 ustawy o VAT.

## simple/verify=off · g-vat-18 (multi, oczekiwane: answer)
**Pytanie:** Kupiłem w 2023 roku maszynę produkcyjną (środek trwały) za 100 000 zł netto i odliczyłem cały VAT, zakładając wykorzystanie wyłącznie do czynności opodatkowanych. W kolejnych latach część produkcji objęto czynnościami zwolnionymi. Czy muszę korygować odliczony podatek?
**Wzorzec:** Tak. Gdy podatnik odliczył cały VAT, a potem zmieniło się prawo do odliczenia (część wykorzystania to czynności zwolnione), stosuje się odpowiednio przepisy o korekcie (art. 91 ust. 7). Dla środka trwałego o wartości początkowej powyżej 15 000 zł korekty dokonuje się w ciągu 5 kolejnych lat, licząc od roku oddania do użytkowania; roczna korekta dotyczy jednej piątej kwoty podatku naliczonego przy nabyciu (art. 91 ust. 2).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 91 ust. 6, VAT art. 91 ust. 3): Na podstawie podanych przepisów nie można jednoznacznie ustalić obowiązku korekty dla tej maszyny, ponieważ nie zawierają one treści VAT art. 91 ust. 1, 2 i 4, które określają zakres korekty dotyczącej takich towarów. Jeżeli maszyna należy do towarów, o których mowa w VAT art. 91 ust. 4, a jej dalsze wykorzystanie obejmuje czynności zwolnione, przy korekcie przyjmuje się dalsze wykorzystanie wyłącznie do czynności zwolnionych (VAT art. 91 ust. 6). Korektę składa się w deklaracji za pierwszy okres rozliczeniowy roku następującego po roku, za który jest dokonywana (VAT art. 91 ust. 3). Podane przepisy nie określają jednak okresu korekty ani sposobu wyliczenia kwoty dla tej maszyny.
**Kontekst:** VAT art. 90a, VAT art. 91 ust. 6, VAT art. 91 ust. 3, VAT art. 99 ust. 7, VAT art. 91 ust. 9
**Sędzia 1** (claude-sonnet-5): partial — System trafnie wskazał obowiązek korekty co do zasady (art. 91 ust. 6 i 3) i uczciwie zasygnalizował, że kontekst nie zawiera ust. 1, 2 i 4 potrzebnych do ustalenia okresu (5 lat) i wysokości korekty (1/5 kwoty), więc nie dopowiedział tych danych spoza kontekstu – ale przez to odpowiedź jest mniej kompletna niż wzorzec, który te liczby podaje.
**Sędzia 2** (gpt-5.6-terra): incorrect — Odpowiedź błędnie stwierdza, że nie można ustalić obowiązku korekty, podczas gdy wzorzec wskazuje obowiązek korekty po zmianie przeznaczenia środka trwałego oraz 5-letni okres i 1/5 rocznie. Jej twierdzenia są jednak oparte wyłącznie na dostępnych w kontekście fragmentach art. 91.

## simple/verify=off · g-vat-20 (multi, oczekiwane: answer)
**Pytanie:** Jestem informatykiem-freelancerem (osoba fizyczna prowadząca jednoosobową działalność, nie spółka) i chcę wystawiać standardowe faktury papierowe moim klientom-firmom bez użycia KSeF — czy to legalne?
**Wzorzec:** Nie — zgodnie z art. 106ga ust. 1 podatnicy są obowiązani wystawiać faktury ustrukturyzowane przy użyciu Krajowego Systemu e-Faktur. Wyjątki od tego obowiązku, określone w art. 106ga ust. 2, dotyczą m.in. podatników bez siedziby w Polsce, sprzedaży na rzecz osób fizycznych nieprowadzących działalności czy korzystających z niektórych procedur szczególnych — żaden z tych wyjątków nie obejmuje zwykłego freelancera fakturującego firmy w Polsce.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 106gb ust. 1, VAT art. 106gb ust. 4, VAT art. 106s): Na podstawie podanych przepisów nie da się rozstrzygnąć, czy możesz legalnie wystawiać klientom-firmom papierowe faktury bez użycia KSeF. Przepisy określają zasady wystawiania faktur ustrukturyzowanych przez KSeF oraz przewidują możliwość określenia przez ministra wyjątków, ale nie podano treści takiego rozporządzenia ani ogólnego przepisu przesądzającego o dopuszczalności papierowych faktur w opisanej sytuacji. Brakuje więc podstawy do oceny Twojego konkretnego przypadku.
**Kontekst:** VAT art. 106s, VAT art. 106gb, VAT art. 106gba, VAT art. 116 ust. 13
**Sędzia 1** (claude-opus-4-7): partial — System odmówił rozstrzygnięcia, choć w kontekście brakowało art. 106ga ust. 1 wprost nakładającego obowiązek — jednak art. 106gb ust. 1 jasno wskazuje, że faktura ustrukturyzowana jest wystawiana przez KSeF, więc można było stwierdzić, że freelancer fakturujący firmy w Polsce nie może używać papierowych faktur. Odpowiedź jest wierna kontekstowi, ale zbyt zachowawcza wobec postawionej tezy wzorca.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W przekazanym kontekście nie ma art. 106ga ustanawiającego obowiązek korzystania z KSeF ani treści rozporządzenia z art. 106s. System prawidłowo wskazał, że na podstawie wyłącznie tych przepisów nie można przesądzić dopuszczalności papierowych faktur w opisanej sytuacji.

## simple/verify=off · g-vat-21 (colloquial, oczekiwane: answer)
**Pytanie:** Wystawiłem klientowi fakturę, ale pomyliłem się w cenie jednostkowej towaru. Czy mogę po prostu wystawić nową, poprawną fakturę zamiast tej błędnej?
**Wzorzec:** Nie — w przypadku stwierdzenia pomyłki w jakiejkolwiek pozycji faktury podatnik wystawia fakturę korygującą, a nie zwykłą nową fakturę zastępującą poprzednią. Faktura korygująca musi zawierać m.in. numer kolejny, datę wystawienia oraz odniesienie do faktury, której dotyczy.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 106j ust. 1 pkt 5, VAT art. 106j ust. 2 pkt 5–6): Pomyłka w cenie jednostkowej jest pomyłką w pozycji faktury, więc podatnik wystawia fakturę korygującą — nie wynika z podanych przepisów możliwość po prostu zastąpienia błędnej faktury nową fakturą. Faktura korygująca powinna zawierać prawidłową treść korygowanej pozycji, a jeżeli korekta zmienia podstawę opodatkowania lub kwotę podatku należnego — także odpowiednią kwotę korekty. 
**Kontekst:** VAT art. 106j, VAT art. 106e ust. 8, VAT art. 106nf
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje konieczność wystawienia faktury korygującej zamiast nowej faktury oraz wymagane elementy (prawidłowa treść pozycji lub kwota korekty), co zgadza się z wzorcem i wynika z cytowanych przepisów art. 106j.
**Sędzia 2** (gpt-5.6-terra): partial — Prawidłowo wskazano obowiązek wystawienia faktury korygującej przy błędzie w cenie jednostkowej. Pominięto jednak podstawowe elementy wskazane we wzorcu (numer, datę i odniesienie do faktury korygowanej), a wymóg podania prawidłowej treści pozycji przedstawiono bez zastrzeżenia, że z art. 106j ust. 2 pkt 6 dotyczy on przypadków innych niż korekty zmieniające podstawę opodatkowania lub podatek.

## simple/verify=off · g-vat-23 (colloquial, oczekiwane: answer)
**Pytanie:** Prowadzę gabinet dentystyczny — czy muszę doliczać VAT do usług leczenia pacjentów?
**Wzorzec:** Nie. Usługi w zakresie opieki medycznej świadczone w ramach wykonywania zawodu lekarza dentysty, służące profilaktyce, zachowaniu, ratowaniu, przywracaniu i poprawie zdrowia, są zwolnione od podatku VAT.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 43 ust. 1 pkt 18, VAT art. 43 ust. 1 pkt 19 lit. a): Usługi leczenia pacjentów są zwolnione z VAT, jeżeli stanowią opiekę medyczną służącą profilaktyce, zachowaniu, ratowaniu, przywracaniu lub poprawie zdrowia i są świadczone w ramach wykonywania zawodu lekarza dentysty (VAT art. 43 ust. 1 pkt 19 lit. a). Zwolnienie może również wynikać z wykonywania tych usług w ramach działalności leczniczej przez podmiot leczniczy (VAT art. 43 ust. 1 pkt 18). Na podstawie podanych informacji nie da się ustalić, czy w Twoim przypadku spełnione są warunki zwolnienia, ponieważ zależy to od statusu podmiotu i charakteru konkretnych świadczeń.
**Kontekst:** VAT art. 43 ust. 1 pkt 14–18a, VAT art. 43 ust. 1 pkt 19–21, VAT art. 131, VAT art. 119, VAT art. 130c
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź trafnie wskazuje zwolnienie z art. 43 ust. 1 pkt 19 lit. a (zawód lekarza dentysty) zgodnie ze wzorcem, dodaje też poprawną informację o alternatywnej podstawie (pkt 18) i nie zawiera treści spoza kontekstu, choć jest mniej jednoznaczna niż wzorzec.
**Sędzia 2** (gpt-5.6-terra): partial — System poprawnie wskazuje warunki zwolnienia z art. 43 ust. 1 pkt 19 lit. a oraz dodatkową podstawę z pkt 18. Nie udziela jednak jednoznacznej odpowiedzi zgodnej ze wzorcem dla usług leczenia wykonywanych przez lekarza dentystę, lecz nadmiernie zastrzega brak możliwości ustalenia zwolnienia.

## simple/verify=off · g-vat-24 (colloquial, oczekiwane: answer)
**Pytanie:** Sprzedaję towar w internecie i pobieram od klienta oprócz ceny towaru także osobną opłatę za koszty przesyłki (wysyłkę kurierem). Czy VAT naliczam tylko od ceny towaru, czy też od kosztów wysyłki?
**Wzorzec:** Od obu kwot łącznie — podstawa opodatkowania obejmuje koszty dodatkowe, takie jak koszty transportu, pobierane przez dokonującego dostawy od nabywcy, więc opłata za przesyłkę wchodzi do podstawy opodatkowania VAT na takich samych zasadach jak cena towaru.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 30b ust. 1, VAT art. 30b ust. 4, VAT art. 30b ust. 5): Podane przepisy nie rozstrzygają ogólnie, czy przy zwykłej sprzedaży internetowej opłata za wysyłkę jest objęta VAT. Jeżeli chodzi o import towarów, koszty transportu i ubezpieczenia do pierwszego miejsca przeznaczenia w kraju, a także koszty transportu do innego znanego w chwili importu miejsca w UE, wchodzą do podstawy opodatkowania, o ile nie zostały już włączone do wartości celnej (VAT art. 30b ust. 4). Ostateczny wynik zależy więc od tego, czy transakcja jest importem oraz od wskazanych w tym przepisie warunków; brak przepisów pozwalających odpowiedzieć na pytanie dla zwykłej sprzedaży krajowej lub unijnej.
**Kontekst:** VAT art. 7a, VAT art. 30b, VAT art. 138f, VAT art. 22 ust. 2, VAT art. 138a
**Sędzia 1** (claude-sonnet-5): refusal_ok — System miał w kontekście tylko art. 30b (podstawa opodatkowania w imporcie), a nie ogólny art. 29a dotyczący zwykłej dostawy towarów, więc słusznie odmówił rozstrzygnięcia dla sprzedaży krajowej/unijnej i oparł się wyłącznie na przepisach, które faktycznie otrzymał, nie dopowiadając niczego z wiedzy ogólnej.
**Sędzia 2** (gpt-5.6-terra): incorrect — System nie odpowiedział na zasadnicze pytanie i ograniczył się do szczególnych reguł importu, podczas gdy wzorzec wskazuje, że koszty transportu pobierane od nabywcy wchodzą do podstawy VAT. Twierdzenia o art. 30b dotyczą importu i wynikają z podanego kontekstu.

## simple/verify=off · g-vat-26 (colloquial, oczekiwane: answer)
**Pytanie:** Otworzyłem warsztat samochodowy i sprzedaję usługi naprawy głównie osobom prywatnym za gotówkę. Czy muszę mieć kasę fiskalną?
**Wzorzec:** Tak, co do zasady — podatnicy dokonujący sprzedaży na rzecz osób fizycznych nieprowadzących działalności gospodarczej oraz rolników ryczałtowych są obowiązani prowadzić ewidencję sprzedaży przy zastosowaniu kas rejestrujących (kas fiskalnych).
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi, czy sprzedaż usług naprawy samochodów na rzecz osób prywatnych za gotówkę wymaga posiadania kasy fiskalnej.
**Kontekst:** PIT art. 12, PIT art. 23 ust. 5b, PIT art. 23 ust. 5
**Sędzia 1** (claude-sonnet-5): refusal_ok — Kontekst dotyczy wyłącznie PIT (przychody pracownicze, samochody), nie zawiera przepisów o kasach fiskalnych (te są w ustawie o VAT), więc słusznie odmówiono odpowiedzi.
**Sędzia 2** (gpt-5.6-terra): incorrect — System bezzasadnie odmówił, choć wzorcowa odpowiedź wskazuje obowiązek ewidencjonowania sprzedaży na rzecz osób prywatnych przy użyciu kas rejestrujących. Odmowa nie dodaje twierdzeń spoza przekazanego kontekstu.

## simple/verify=off · g-pit-07 (fact, oczekiwane: answer)
**Pytanie:** Jaką stawkę podatku dochodowego stosuje się do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia?
**Wzorzec:** Podatek dochodowy od dochodu z odpłatnego zbycia nieruchomości i praw określonych w art. 10 ust. 1 pkt 8 lit. a–c wynosi 19% podstawy obliczenia podatku.
**Odpowiedź** (odmowa=True; cytaty: PIT art. 21 ust. 1 pkt 29, PIT art. 21 ust. 1 pkt 131): W przepisach, które mam, nie ma odpowiedzi, jaką stawkę podatku dochodowego stosuje się do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia. Podane przepisy określają jedynie niektóre zwolnienia, w tym dotyczące dochodów z odpłatnego zbycia nieruchomości (PIT art. 21 ust. 1 pkt 29 i PIT art. 21 ust. 1 pkt 131).
**Kontekst:** PIT art. 21 ust. 1 pkt 29, PIT art. 21 ust. 39, PIT art. 21 ust. 1 pkt 29a, PIT art. 21 ust. 1 pkt 131–133, VAT art. 62
**Sędzia 1** (claude-sonnet-5): refusal_missing — Kontekst nie zawiera art. 30e PIT ze stawką 19%, więc system nie mógł podać prawidłowej odpowiedzi — ale sama odmowa jest zgodna z dostępnymi przepisami, więc jest to błąd luki w kontekście, nie systemu; mimo to oczekiwano odpowiedzi merytorycznej, której brak.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W udostępnionych przepisach nie ma stawki 19% ani treści art. 30e ustawy PIT; wskazano jedynie zwolnienia. Odmowa podania stawki była więc prawidłowa przy ograniczeniu do kontekstu.

## simple/verify=off · g-op-09 (multi, oczekiwane: answer)
**Pytanie:** Czy wniesienie skargi do sądu administracyjnego na decyzję podatkową wpływa na bieg 5-letniego terminu przedawnienia zobowiązania podatkowego?
**Wzorzec:** Tak. Zobowiązanie podatkowe przedawnia się co do zasady z upływem 5 lat od końca roku, w którym upłynął termin płatności podatku, ale bieg tego terminu nie rozpoczyna się, a rozpoczęty ulega zawieszeniu z dniem wniesienia skargi do sądu administracyjnego na decyzję dotyczącą tego zobowiązania.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 70e § 1–2, Ordynacja art. 70 § 7 pkt 2, Ordynacja art. 68 § 2–3): Z podanych przepisów wynika, że w postępowaniu dotyczącym decyzji określającej warunki cofnięcia skutków unikania opodatkowania wniesienie skargi do sądu administracyjnego przedłuża zawieszenie biegu terminu przedawnienia do dnia następującego po doręczeniu organowi podatkowemu odpisu prawomocnego orzeczenia sądu administracyjnego (Ordynacja art. 70e § 2). W ogólnym przypadku skargi na decyzję podatkową podane przepisy nie określają, czy samo wniesienie skargi zawiesza lub w inny sposób wpływa na pięcioletni termin przedawnienia; wskazują jedynie, że po doręczeniu organowi odpisu prawomocnego orzeczenia bieg terminu rozpoczyna się albo biegnie dalej (Ordynacja art. 70 § 7 pkt 2).
**Kontekst:** Ordynacja art. 68, Ordynacja art. 69, Ordynacja art. 70e, Ordynacja art. 70 § 1b, Ordynacja art. 70 § 7
**Sędzia 1** (claude-sonnet-5): refusal_ok — Dostarczony kontekst nie zawiera ogólnego przepisu (art. 70 § 6 pkt 2) stanowiącego, że wniesienie skargi do sądu administracyjnego zawiesza bieg przedawnienia zobowiązania podatkowego - system trafnie to zauważył i nie zmyślił odpowiedzi 'Tak', ograniczając się do opisania specyficznego przypadku z art. 70e (unikanie opodatkowania) i odesłania do art. 70 § 7 pkt 2, co jest zgodne z posiadanym materiałem.
**Sędzia 2** (gpt-5.6-terra): incorrect — Odpowiedź błędnie twierdzi, że przepisy nie określają wpływu zwykłej skargi na decyzję podatkową. Art. 70 § 7 pkt 2 wprost zakłada zawieszenie i stanowi, że bieg terminu rozpoczyna się albo biegnie dalej od dnia po doręczeniu organowi prawomocnego orzeczenia sądu.

## simple/verify=off · g-ooc-02 (out_of_corpus, oczekiwane: refuse)
**Pytanie:** Napisz mi krótki wiersz o jesieni.
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie — nie dotyczy ono prawa podatkowego, a zajmuję się wyłącznie przepisami podatkowymi.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na prośbę o napisanie wiersza o jesieni.
**Kontekst:** VAT art. 2 pkt 27g–28, PIT art. 5a pkt 36–40, Ordynacja art. 12, PIT art. 52ub, PIT art. 30h
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie odmówił odpowiedzi na pytanie niepodatkowe, zgodnie z zakresem przepisów, tak jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił odpowiedzi na pytanie pozapodatkowe, zgodnie z oczekiwanym zachowaniem. Nie dodał żadnych twierdzeń spoza przekazanego kontekstu.

## simple/verify=off · g-ooc-05 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaki jest podatek PCC od zakupu mieszkania z rynku wtórnego?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Podatek od czynności cywilnoprawnych (PCC), w tym jego stawkę przy zakupie nieruchomości, reguluje ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej podatku PCC od zakupu mieszkania z rynku wtórnego.
**Kontekst:** VAT art. 10, VAT art. 13, VAT art. 26, Ordynacja art. 285a, VAT art. 7
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, bo PCC nie jest w przepisach VAT/PIT/Ordynacja; odpowiedź nie dodaje żadnych faktów spoza kontekstu, choć nie wskazuje wprost właściwej ustawy jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo odmówił odpowiedzi, ponieważ przekazane przepisy nie regulują PCC ani jego stawki przy zakupie mieszkania. Nie dodał żadnych informacji spoza kontekstu.

## simple/verify=off · g-ooc-12 (out_of_corpus, oczekiwane: answer_with_date)
**Pytanie:** Jaki limit zwolnienia podmiotowego z VAT będzie obowiązywał w 2028 roku?
**Wzorzec:** Mam dostęp do ustawy o VAT w stanie prawnym na 2026-08-26. Obecnie (stan na tę datę) limit zwolnienia podmiotowego z VAT wynosi 240 000 zł (art. 113 ust. 1 ustawy o VAT). Korpus nie zawiera żadnego przepisu przejściowego ani zapowiedzi zmiany tego limitu na 2028 rok, więc nie mogę potwierdzić, czy i jak zmieni się on w przyszłości.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na pytanie o limit zwolnienia podmiotowego z VAT obowiązujący w 2028 roku.
**Kontekst:** VAT art. 43 ust. 24, VAT art. 81, VAT art. 43 ust. 20, VAT art. 56 ust. 2, VAT art. 52
**Sędzia 1** (claude-sonnet-5): refusal_ok — System trafnie odmówił, bo w jego kontekście brak art. 113 o limicie zwolnienia podmiotowego i brak jakiejkolwiek daty stanu prawnego - nie dopowiedział niczego spoza przepisów, choć nie podał aktualnego limitu 2026 (co i tak nie było w jego kontekście).
**Sędzia 2** (gpt-5.6-terra): partial — System słusznie stwierdza, że przekazany kontekst nie zawiera przepisu określającego limit na 2028 r. Nie podaje jednak stanu prawnego według daty korpusu ani obowiązującego obecnie limitu, czego oczekiwano.

## simple/verify=off · g-ooc-18 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy od sprzedaży laptopa prywatnie (jako osoba fizyczna, nieprowadząca działalności) muszę zapłacić VAT i jak długo trzeba przechowywać taką transakcję w ewidencji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 15 ust. 1 wskazuje, że podatnikami VAT są podmioty wykonujące samodzielnie działalność gospodarczą — skoro sprzedaje Pan prywatny przedmiot poza taką działalnością, nie jest Pan podatnikiem VAT z tego tytułu, więc VAT nie wystąpi. Natomiast szczegółowe zasady przechowywania ewidencji/dokumentów przez osoby prywatne nieprowadzące działalności nie są uregulowane w ustawie o VAT (ta reguluje obowiązki podatników VAT, a Pan nim nie jest w tej transakcji) — to wykracza poza mój korpus i nie mogę podać odpowiedzi w tej części.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 111 ust. 1, VAT art. 111 ust. 3a pkt 6): W podanych przepisach nie ma odpowiedzi, czy prywatna sprzedaż laptopa przez osobę fizyczną nieprowadzącą działalności podlega VAT, ponieważ nie określają one, czy taka osoba jest w tej sytuacji podatnikiem. Jeżeli sprzedaż byłaby sprzedażą dokonywaną przez podatnika na rzecz osoby fizycznej nieprowadzącej działalności, przepisy przewidują obowiązek ewidencjonowania sprzedaży przy zastosowaniu kasy rejestrującej (VAT art. 111 ust. 1). Przepisy wskazują, że kopie dokumentów kasowych przechowuje się przez okres wymagany w art. 112, ale treści art. 112 nie podano, więc nie można ustalić okresu przechowywania tej transakcji na podstawie dostępnych przepisów (VAT art. 111 ust. 3a pkt 6).
**Kontekst:** VAT art. 111 ust. 6, VAT art. 111 ust. 1, VAT art. 111 ust. 4, VAT art. 111 ust. 3a pkt 1–11, VAT art. 138i, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): incorrect — System błędnie stwierdza, że z przepisów nie wynika, czy osoba prywatna jest podatnikiem (podczas gdy art. 15 ust. 1, obecny w korpusie wzorcowym, daje tu jasną odpowiedź - prywatna sprzedaż poza działalnością gospodarczą nie podlega VAT), a następnie dopowiada nieistniejący w podanym kontekście scenariusz sprzedaży przez 'podatnika' i kasy fiskalne, co jest spoza tematu pytania i wprowadza w błąd.
**Sędzia 2** (gpt-5.6-terra): partial — Odpowiedź prawidłowo wskazuje, że z przytoczonych przepisów nie da się ustalić okresu przechowywania, ale błędnie odmawia rozstrzygnięcia VAT zamiast wskazać, że prywatna sprzedaż poza działalnością nie czyni sprzedawcy podatnikiem VAT. Dodatkowo opis kasy fiskalnej jest tylko warunkowy i nie odpowiada na stan faktyczny.

## simple/verify=off · g-ooc-19 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy odsetki za zwłokę w podatku są wysokie i czy mogę zapłacić je kartą płatniczą w urzędzie?
**Wzorzec:** Stawka odsetek za zwłokę to suma 200% podstawowej stopy kredytu lombardowego NBP i 2%, nie mniej niż 8% (Ordynacja art. 56 § 1). Co do zapłaty kartą: Ordynacja dopuszcza zapłatę „innym instrumentem płatniczym” za pośrednictwem konta w e-Urzędzie Skarbowym (art. 61 § 1 pkt 2); zasad płacenia kartą bezpośrednio w kasie urzędu w korpusie nie ma.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 53 § 1 i 3, Ordynacja art. 55 § 1, Ordynacja art. 56b): Przepisy nie podają podstawowej stawki odsetek, więc na ich podstawie nie można ocenić, czy są one „wysokie”; od zaległości podatkowych nalicza się odsetki za zwłokę, które podatnik nalicza i wpłaca bez wezwania organu podatkowego (Ordynacja art. 53 § 1 i 3, art. 55 § 1). W podatku od towarów i usług oraz podatku akcyzowym może mieć zastosowanie podwyższona stawka w wysokości 150% stawki odsetek, ale tylko w warunkach określonych w przepisie (Ordynacja art. 56b). W podanych przepisach nie ma informacji, czy odsetki można zapłacić kartą płatniczą w urzędzie.
**Kontekst:** Ordynacja art. 55, Ordynacja art. 53, Ordynacja art. 56b, Ordynacja art. 76
**Sędzia 1** (claude-sonnet-5): partial — System poprawnie odmówił oceny 'wysokości' i kwestii karty z powodu braku odpowiednich przepisów w kontekście, ale błędnie stwierdził, że przepisy nie podają stawki odsetek - podczas gdy art. 56 § 1 (suma 200% stopy lombardowej + 2%, min. 8%) po prostu nie znalazł się w jego kontekście, mimo że wzorzec wskazuje, że powinien tam być; system poprawnie wskazał brak informacji o karcie, ale nie podał żadnej konkretnej stawki odsetek, co jest istotnym pominięciem względem wzorca.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź trafnie wskazuje, że w przekazanym kontekście nie ma podstawowej stawki odsetek, więc nie można ocenić ich wysokości, oraz że brak jest informacji o płatności kartą w urzędzie. Informacja o stawce 150% dla VAT i akcyzy jest zgodna z art. 56b.

## simple/verify=off · g-ooc-20 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Sprzedaję używany budynek biurowy, który był zasiedlony 5 lat temu — czy ta dostawa jest zwolniona z VAT, i jaką stawkę PCC zapłaci kupujący od tej transakcji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 43 ust. 1 pkt 10 zwalnia od podatku dostawę budynków, budowli lub ich części, z wyjątkiem dostawy w ramach pierwszego zasiedlenia lub przed nim, oraz dostawy dokonanej w ciągu 2 lat od pierwszego zasiedlenia. Skoro budynek był zasiedlony 5 lat temu (czyli upłynęły więcej niż 2 lata), dostawa korzysta ze zwolnienia z VAT na podstawie tego przepisu. Natomiast kwestia podatku od czynności cywilnoprawnych (PCC), który może obciążać kupującego przy zakupie nieruchomości zwolnionej z VAT, nie jest uregulowana w ustawie o VAT — reguluje ją ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu, więc nie mogę podać stawki PCC.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 43 ust. 10): Na podstawie podanych przepisów nie można stwierdzić, czy dostawa budynku jest zwolniona z VAT, ponieważ nie udostępniono VAT art. 43 ust. 1 pkt 10, do którego odwołuje się VAT art. 43 ust. 10; można jedynie wskazać, że rezygnacja z tego zwolnienia wymaga, aby sprzedający i nabywca byli zarejestrowani jako podatnicy VAT czynni oraz złożyli zgodne oświadczenie w wymaganej formie. Wśród podanych przepisów nie ma regulacji dotyczących podatku od czynności cywilnoprawnych ani stawki PCC, więc nie można określić kwoty ani stawki PCC dla kupującego.
**Kontekst:** VAT art. 43 ust. 10, VAT art. 63, VAT art. 61, VAT art. 7, VAT art. 103 ust. 5a
**Sędzia 1** (claude-sonnet-5): incorrect — System odmówił odpowiedzi na część VAT, mimo że kluczowy przepis (art. 43 ust. 1 pkt 10, treść zwolnienia) znajduje się faktycznie w kontekście w postaci cytatu/odniesienia w art. 43 ust. 10 - system błędnie stwierdził, że nie ma tego przepisu, podczas gdy z udostępnionych fragmentów (choć bez pełnej treści pkt 10) nie da się jednoznacznie odtworzyć zwolnienia, więc odmowa w części VAT jest nadmierna/błędna wobec wzorca, który wprost podaje zwolnienie na podstawie tego przepisu.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W kontekście nie ma art. 43 ust. 1 pkt 10, więc nie można ustalić, czy sprzedaż po 5 latach korzysta ze zwolnienia z VAT. System prawidłowo wskazał też brak przepisów o PCC i wiernie opisał warunki rezygnacji ze zwolnienia wynikające z art. 43 ust. 10.

## hybrid/verify=off · g-vat-08 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie urząd skarbowy powinien zwrócić podatnikowi różnicę podatku VAT (nadwyżkę podatku naliczonego nad należnym) na rachunek bankowy?
**Wzorzec:** Zwrot różnicy podatku następuje w terminie 40 dni od dnia złożenia rozliczenia przez podatnika, z zastrzeżeniem wyjątków wskazanych w ust. 6, 6a i 6d art. 87.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 87 ust. 2, VAT art. 87 ust. 6 pkt 1–3, VAT art. 87 ust. 6a): Co do zasady urząd skarbowy powinien zwrócić różnicę podatku w terminie 40 dni od dnia złożenia rozliczenia na rachunek bankowy podatnika (VAT art. 87 ust. 2). Termin wynosi 25 dni, jeżeli łącznie spełnione są warunki określone w VAT art. 87 ust. 6 pkt 1–3. Na wniosek podatnika zawarty w deklaracji zwrot na rachunek VAT następuje w terminie 25 dni (VAT art. 87 ust. 6a). Jeżeli zasadność zwrotu wymaga dodatkowego zweryfikowania, naczelnik urzędu skarbowego może przedłużyć termin do zakończenia weryfikacji (VAT art. 87 ust. 2).
**Kontekst:** VAT art. 87 ust. 2, VAT art. 87 ust. 6 pkt 1–3, VAT art. 87 ust. 6a, VAT art. 112b, VAT art. 87 ust. 1
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje podstawowy termin 40 dni i dodatkowo trafnie uzupełnia o wyjątki (25 dni, przedłużenie przy weryfikacji) zgodnie z przepisami w kontekście, co jest zgodne z zastrzeżeniem ust. 6, 6a, 6d we wzorcu.
**Sędzia 2** (gpt-5.6-terra): partial — Prawidłowo wskazano zasadniczy termin 40 dni oraz wyjątki 25-dniowe i możliwość przedłużenia weryfikacji. Odpowiedź pomija jednak zastrzeżenie dotyczące art. 87 ust. 6d, wyraźnie wskazane w ust. 2 i we wzorcu.

## hybrid/verify=off · g-vat-13 (multi, oczekiwane: answer)
**Pytanie:** Spółka A i spółka B należą do tej samej grupy VAT. Czy sprzedaż towarów między nimi podlega opodatkowaniu VAT?
**Wzorzec:** Nie — dostawa towarów i świadczenie usług dokonane przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlegają opodatkowaniu (art. 8c ust. 1), o ile spółki A i B tworzą grupę VAT w rozumieniu art. 2 pkt 47, czyli grupę podmiotów powiązanych finansowo, ekonomicznie i organizacyjnie, zarejestrowaną jako podatnik podatku.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 8c ust. 1): Nie. Dostawa towarów dokonana przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlega opodatkowaniu VAT (VAT art. 8c ust. 1).
**Kontekst:** VAT art. 8c, VAT art. 14 ust. 7, Ordynacja art. 86a § 6
**Sędzia 1** (claude-sonnet-5): partial — Poprawnie wskazuje art. 8c ust. 1 i brak opodatkowania, ale pomija świadczenie usług oraz warunek, że A i B muszą faktycznie tworzyć grupę VAT w rozumieniu art. 2 pkt 47 (co wzorzec zaznacza).
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje, że dostawa towarów między członkami tej samej grupy VAT nie podlega opodatkowaniu, zgodnie z art. 8c ust. 1 ustawy o VAT.

## hybrid/verify=off · g-vat-22 (colloquial, oczekiwane: answer)
**Pytanie:** Mam mały warzywniak i kupiłem nowy samochód osobowy do rozwożenia towaru do klientów, ale czasem jeżdżę nim też prywatnie. Mogę odliczyć cały VAT z faktury za auto?
**Wzorzec:** Nie w pełni — jeśli samochód jest używany również do celów prywatnych (nie wyłącznie do działalności), przysługuje odliczenie tylko 50% kwoty podatku naliczonego z faktury. Pełne odliczenie byłoby możliwe tylko, gdyby pojazd był wykorzystywany wyłącznie do działalności gospodarczej, co trzeba dodatkowo potwierdzić ewidencją przebiegu pojazdu.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 86a ust. 9): Na podstawie podanych przepisów nie można stwierdzić, czy możesz odliczyć cały VAT z faktury za samochód. VAT art. 86a ust. 9 wymienia określone pojazdy inne niż samochody osobowe, ale w przekazanych przepisach brakuje regulacji określających zakres odliczenia dla samochodu osobowego używanego także prywatnie.
**Kontekst:** VAT art. 106b, VAT art. 114, VAT art. 86a ust. 9, VAT art. 86 ust. 8, VAT art. 113 ust. 13, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): refusal_missing — System odmówił odpowiedzi, mimo że kontekst (choć bez kluczowego art. 86a ust. 1 i 3 o limicie 50%) nie zawiera przepisu wprost regulującego tę kwestię — jednak oczekiwano merytorycznej odpowiedzi o 50% odliczeniu, więc dostępne fragmenty były niewystarczające, ale odmowa była nadmiarowa względem oczekiwanego zachowania; system słusznie nie dopowiedział faktów spoza kontekstu.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W kontekście nie ma art. 86a ust. 1–4 regulujących limit 50% i warunki pełnego odliczenia VAT dla samochodów osobowych. System trafnie wskazał, że sam ust. 9 dotyczy wyłącznie określonych pojazdów innych niż osobowe.

## hybrid/verify=off · g-vat-24 (colloquial, oczekiwane: answer)
**Pytanie:** Sprzedaję towar w internecie i pobieram od klienta oprócz ceny towaru także osobną opłatę za koszty przesyłki (wysyłkę kurierem). Czy VAT naliczam tylko od ceny towaru, czy też od kosztów wysyłki?
**Wzorzec:** Od obu kwot łącznie — podstawa opodatkowania obejmuje koszty dodatkowe, takie jak koszty transportu, pobierane przez dokonującego dostawy od nabywcy, więc opłata za przesyłkę wchodzi do podstawy opodatkowania VAT na takich samych zasadach jak cena towaru.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 22 ust. 1 pkt 1–4, VAT art. 22 ust. 2, VAT art. 22 ust. 2a, VAT art. 22 ust. 2b): W podanych przepisach nie ma regulacji dotyczącej tego, czy osobna opłata za przesyłkę powiększa podstawę opodatkowania VAT, dlatego na ich podstawie nie można rozstrzygnąć, czy VAT nalicza się także od kosztów wysyłki. Przepisy te określają jedynie miejsce dostawy towarów wysyłanych lub transportowanych oraz zasady przyporządkowania transportu przy kolejnych dostawach, a nie sposób opodatkowania opłaty za przesyłkę.
**Kontekst:** VAT art. 22 ust. 1 pkt 1–4, VAT art. 138a, VAT art. 22 ust. 2a, VAT art. 22 ust. 2, VAT art. 22 ust. 2b
**Sędzia 1** (claude-sonnet-5): refusal_missing — System trafnie stwierdził, że podane przepisy (dotyczące miejsca dostawy) nie regulują podstawy opodatkowania, ale w rzeczywistości odpowiedź istnieje w przepisach VAT (art. 29a) – system powinien był dostać ten przepis w kontekście, więc odmowa jest nieoczekiwana wobec dostępnej wiedzy prawnej, choć wobec faktycznie dostarczonego kontekstu jest to poprawna i wierna odmowa.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — Kontekst zawiera wyłącznie przepisy o miejscu dostawy i przyporządkowaniu transportu, a nie o podstawie opodatkowania ani kosztach dodatkowych. System prawidłowo wskazał, że na tej podstawie nie da się rozstrzygnąć kwestii VAT od przesyłki.

## hybrid/verify=off · g-pit-03 (fact, oczekiwane: answer)
**Pytanie:** Jaką stawkę podatku liniowego stosuje się do dochodów z pozarolniczej działalności gospodarczej, jeśli podatnik wybrał ten sposób opodatkowania?
**Wzorzec:** Podatek dochodowy liniowy od dochodów z pozarolniczej działalności gospodarczej lub działów specjalnych produkcji rolnej wynosi 19% podstawy obliczenia podatku.
**Odpowiedź** (odmowa=True; cytaty: PIT art. 9a ust. 2, PIT art. 30ca ust. 1): W podanych przepisach nie ma ogólnej stawki podatku liniowego dla dochodów z pozarolniczej działalności gospodarczej; wskazano jedynie możliwość wyboru opodatkowania na zasadach określonych w art. 30c (PIT art. 9a ust. 2). Stawka 5% dotyczy wyłącznie kwalifikowanego dochodu z kwalifikowanych praw własności intelektualnej (PIT art. 30ca ust. 1), a nie ogólnie dochodów z działalności gospodarczej. W przepisach, które mam, nie ma odpowiedzi na pytanie o ogólną stawkę podatku liniowego.
**Kontekst:** PIT art. 9a, PIT art. 44 ust. 7f, PIT art. 44 ust. 6b, PIT art. 26gb, PIT art. 30ca ust. 1
**Sędzia 1** (claude-sonnet-5): refusal_missing — System odmówił, choć w jego własnym kontekście brakuje jedynie art. 30c samego w sobie (treść stawki), lecz skoro brak tego przepisu w dostarczonym kontekście, odmowa faktycznie jest zasadna – system nie miał dostępu do treści art. 30c ust. 1 ze stawką 19%, więc nie mógł podać poprawnej odpowiedzi bez wykraczania poza kontekst.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W przekazanym kontekście nie ma treści art. 30c PIT, która określa stawkę liniową 19%, więc system nie mógł jej podać bez wychodzenia poza kontekst. Prawidłowo wskazał jedynie odesłanie do art. 30c oraz odróżnił stawkę 5% z art. 30ca.

## hybrid/verify=off · g-pit-14 (colloquial, oczekiwane: answer)
**Pytanie:** Pracuję na jednym etacie w tej samej miejscowości, w której mieszkam — o ile mogę pomniejszyć swój przychód z tytułu kosztów uzyskania przychodu w ciągu roku?
**Wzorzec:** Przy jednym stosunku pracy w miejscowości zamieszkania koszty uzyskania przychodów wynoszą 250 zł miesięcznie, czyli maksymalnie 3000 zł za cały rok podatkowy.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 22 ust. 2 pkt 1, PIT art. 22 ust. 2 pkt 3, PIT art. 22 ust. 11): Możesz pomniejszyć przychód o koszty uzyskania przychodów w wysokości 250 zł miesięcznie, jednak za rok podatkowy łącznie nie więcej niż 3000 zł, ponieważ uzyskujesz przychody z tytułu jednego stosunku pracy. Nie ma podstaw do zastosowania podwyższonego limitu dotyczącego zamieszkania poza miejscowością zakładu pracy. Jeżeli roczne koszty są niższe od faktycznie poniesionych i udokumentowanych imiennymi biletami okresowymi wydatków na dojazd, w rocznym rozliczeniu możesz przyjąć koszty w wysokości tych wydatków.
**Kontekst:** PIT art. 22 ust. 2, PIT art. 22 ust. 1kc, PIT art. 22 ust. 9 pkt 5–6, PIT art. 22i, PIT art. 22 ust. 11
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zawiera prawidłową kwotę 250 zł/mies. i 3000 zł rocznie zgodnie z wzorcem, dodatkowo trafnie wyjaśnia wykluczenie podwyższonego limitu oraz możliwość uwzględnienia wyższych udokumentowanych wydatków na dojazd — wszystko oparte na przepisach z kontekstu.
**Sędzia 2** (gpt-5.6-terra): partial — Prawidłowo wskazano podstawowe koszty 250 zł miesięcznie i limit 3000 zł rocznie oraz brak podstaw do podwyższonego limitu. Przy wyjątku dotyczącym dojazdów pominięto istotny warunek, że chodzi wyłącznie o przejazdy transportem autobusowym, kolejowym, promowym lub komunikacją miejską, więc ujęto go zbyt szeroko.

## hybrid/verify=off · g-op-02 (fact, oczekiwane: answer)
**Pytanie:** Jaka jest wysokość stawki odsetek za zwłokę od zaległości podatkowych?
**Wzorzec:** Stawka odsetek za zwłokę jest równa sumie 200% podstawowej stopy oprocentowania kredytu lombardowego i 2%, z tym że nie może być niższa niż 8%.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 53 § 1, Ordynacja art. 56a § 1, Ordynacja art. 56b): W podanych przepisach nie określono podstawowej wysokości stawki odsetek za zwłokę. Określono jedynie stawkę obniżoną jako 50% stawki podstawowej, przy spełnieniu wskazanych warunków, oraz stawkę podwyższoną jako 150% stawki podstawowej w określonych przypadkach (Ordynacja art. 56a § 1; Ordynacja art. 56b).
**Kontekst:** Ordynacja art. 56a, Ordynacja art. 56b, Ordynacja art. 53, Ordynacja art. 55, Ordynacja art. 57
**Sędzia 1** (claude-sonnet-5): refusal_ok — Przepis definiujący podstawową stawkę odsetek (art. 56 Ordynacji) nie znajduje się w podanym kontekście, więc system prawidłowo odmówił podania konkretnej wartości i trafnie opisał jedynie dostępne w kontekście stawki obniżoną i podwyższoną.
**Sędzia 2** (gpt-5.6-terra): incorrect — Odpowiedź nie podaje wymaganej podstawowej stawki, choć według wzorca wynosi ona 200% stopy lombardowej plus 2%, nie mniej niż 8%. Twierdzenia o stawce obniżonej i podwyższonej są jednak zgodne z przepisami przekazanymi w kontekście.

## hybrid/verify=off · g-op-03 (fact, oczekiwane: answer)
**Pytanie:** Co uznaje się za nadpłatę podatku zgodnie z Ordynacją podatkową?
**Wzorzec:** Za nadpłatę uważa się m.in. kwotę nadpłaconego lub nienależnie zapłaconego podatku oraz kwotę podatku pobraną przez płatnika nienależnie lub w wysokości większej od należnej.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 72 § 1, Ordynacja art. 72 § 1a, Ordynacja art. 72 § 1b, Ordynacja art. 72 § 2): Za nadpłatę uważa się kwotę nadpłaconego lub nienależnie zapłaconego podatku, a także podatek pobrany przez płatnika nienależnie albo w kwocie wyższej od należnej. Nadpłatą jest również zobowiązanie zapłacone przez płatnika, inkasenta, osobę trzecią lub spadkobiercę, jeżeli określono je jako nienależne albo w wysokości wyższej od należnej. Na równi z nadpłatą traktuje się także określoną różnicę wykazaną w zeznaniu PIT, kwoty przysługujące na podstawie wskazanych ulg oraz część wpłaty zaliczoną na odsetki za zwłokę, a także nienależnie zapłacone zaległości, odsetki od nieterminowych zaliczek i opłatę prolongacyjną.
**Kontekst:** Ordynacja art. 77c, Ordynacja art. 72, Ordynacja art. 77b, Ordynacja art. 76a, Ordynacja art. 75
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź systemu poprawnie i dokładnie referuje art. 72 § 1, 1a, 1b i 2, zawierając wszystkie elementy wzorca oraz dodatkowe szczegóły zgodne z przepisami w kontekście, bez błędów.
**Sędzia 2** (gpt-5.6-terra): partial — Odpowiedź prawidłowo podaje podstawowe przypadki z art. 72 § 1, ale przy zobowiązaniach płatnika, inkasenta, osoby trzeciej i spadkobiercy pomija istotny warunek określenia ich w odpowiedniej decyzji. Zbyt ogólnie opisuje też szczególne kwoty traktowane na równi z nadpłatą, lecz nie dodaje twierdzeń sprzecznych z kontekstem.

## hybrid/verify=off · g-ooc-02 (out_of_corpus, oczekiwane: refuse)
**Pytanie:** Napisz mi krótki wiersz o jesieni.
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie — nie dotyczy ono prawa podatkowego, a zajmuję się wyłącznie przepisami podatkowymi.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na prośbę o napisanie wiersza o jesieni.
**Kontekst:** PIT art. 5a pkt 36–40, Ordynacja art. 294, PIT art. 22j ust. 8, PIT art. 24 ust. 13, VAT art. 2 pkt 27g–28
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie odmówił odpowiedzi na pytanie niepodatkowe, zgodnie z zakresem przepisów, tak jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił odpowiedzi na pytanie pozapodatkowe, zgodnie z oczekiwanym zachowaniem. Nie dodał żadnych twierdzeń spoza przekazanego kontekstu.

## hybrid/verify=off · g-ooc-05 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaki jest podatek PCC od zakupu mieszkania z rynku wtórnego?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Podatek od czynności cywilnoprawnych (PCC), w tym jego stawkę przy zakupie nieruchomości, reguluje ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej podatku PCC od zakupu mieszkania z rynku wtórnego.
**Kontekst:** PIT art. 24 ust. 24, VAT art. 10, PIT art. 26 ust. 7a pkt 1–6b, VAT art. 13, VAT art. 111 ust. 7b
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, bo PCC nie jest w przepisach VAT/PIT/Ordynacja; odpowiedź nie dodaje żadnych faktów spoza kontekstu, choć nie wskazuje wprost właściwej ustawy jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo odmówił odpowiedzi, ponieważ przekazane przepisy nie regulują PCC ani jego stawki przy zakupie mieszkania. Nie dodał żadnych informacji spoza kontekstu.

## hybrid/verify=off · g-ooc-08 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jakie są stawki ryczałtu od przychodów ewidencjonowanych dla usług budowlanych?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki ryczałtu od przychodów ewidencjonowanych reguluje ustawa o zryczałtowanym podatku dochodowym od niektórych przychodów osiąganych przez osoby fizyczne, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: PIT art. 9a, PIT art. 24b ust. 2 pkt 2): W przepisach, które mam, nie ma odpowiedzi na pytanie o stawki ryczałtu od przychodów ewidencjonowanych dla usług budowlanych. PIT art. 9a wskazuje jedynie, że ryczałt jest określony w ustawie o zryczałtowanym podatku dochodowym, której treści nie podano; PIT art. 24b ust. 2 pkt 2 dotyczy wyłącznie wskaźnika dochodu przy jego oszacowaniu, a nie stawki ryczałtu.
**Kontekst:** PIT art. 22i, PIT art. 9a, VAT art. 41 ust. 12, PIT art. 29, PIT art. 24b
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, trafnie wskazując że stawki ryczałtu są regulowane w ustawie o zryczałtowanym podatku dochodowym spoza kontekstu, i prawidłowo odróżnił to od niezwiązanego art. 24b (wskaźnik szacowania dochodu).
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo odmówił podania stawek, wskazując, że PIT art. 9a odsyła w tej kwestii do ustawy o zryczałtowanym podatku dochodowym, której nie ma w kontekście. Trafnie odróżnił wskaźnik 10% z art. 24b ust. 2 pkt 2 od stawki ryczałtu.

## hybrid/verify=off · g-ooc-09 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaka jest stawka podatku od nieruchomości za metr kwadratowy budynku mieszkalnego?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki podatku od nieruchomości reguluje ustawa o podatkach i opłatach lokalnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej stawki podatku od nieruchomości za metr kwadratowy budynku mieszkalnego.
**Kontekst:** VAT art. 41 ust. 12b, PIT art. 22g ust. 10, VAT art. 41 ust. 12, PIT art. 30g ust. 8, VAT art. 41 ust. 12a
**Sędzia 1** (claude-sonnet-5): correct — System prawidłowo odmówił odpowiedzi, wskazując że przepisy VAT/PIT/Ordynacja nie zawierają stawek podatku od nieruchomości; nie dopowiedział niczego spoza kontekstu, choć nie wskazał wprost ustawy o podatkach i opłatach lokalnych jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił, ponieważ w przekazanych przepisach nie ma stawki podatku od nieruchomości za m² budynku mieszkalnego. Nie dodał żadnych informacji spoza kontekstu.

## hybrid/verify=off · g-ooc-10 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Ile kosztuje opłata skarbowa za pełnomocnictwo złożone w urzędzie skarbowym?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Wysokość opłaty skarbowej za pełnomocnictwo reguluje ustawa o opłacie skarbowej, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: Ordynacja art. 80a § 2, Ordynacja art. 138d § 3): W udostępnionych przepisach nie ma informacji o wysokości opłaty skarbowej za pełnomocnictwo złożone w urzędzie skarbowym. Przepisy określają jedynie zasady składania pełnomocnictw, ale nie regulują tej opłaty.
**Kontekst:** Ordynacja art. 299 § 6a, Ordynacja art. 14za, Ordynacja art. 80a, Ordynacja art. 138d
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, trafnie wskazując że kontekst (Ordynacja) nie zawiera informacji o wysokości opłaty skarbowej, choć nie wskazał konkretnej ustawy o opłacie skarbowej jako źródła - wzorzec sugerował to jako plus, ale brak tego nie czyni odpowiedzi błędną.
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo odmówił podania kwoty, ponieważ udostępnione przepisy nie regulują wysokości opłaty skarbowej za pełnomocnictwo. Wskazanie, że kontekst dotyczy jedynie zasad składania pełnomocnictw, wynika z przytoczonych przepisów Ordynacji.

## hybrid/verify=off · g-ooc-12 (out_of_corpus, oczekiwane: answer_with_date)
**Pytanie:** Jaki limit zwolnienia podmiotowego z VAT będzie obowiązywał w 2028 roku?
**Wzorzec:** Mam dostęp do ustawy o VAT w stanie prawnym na 2026-08-26. Obecnie (stan na tę datę) limit zwolnienia podmiotowego z VAT wynosi 240 000 zł (art. 113 ust. 1 ustawy o VAT). Korpus nie zawiera żadnego przepisu przejściowego ani zapowiedzi zmiany tego limitu na 2028 rok, więc nie mogę potwierdzić, czy i jak zmieni się on w przyszłości.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na pytanie o limit zwolnienia podmiotowego z VAT obowiązujący w 2028 roku. Podane przepisy dotyczą innych zwolnień i nie określają tego limitu.
**Kontekst:** VAT art. 52, VAT art. 43 ust. 24, VAT art. 43 ust. 5, VAT art. 43 ust. 23, VAT art. 80
**Sędzia 1** (claude-sonnet-5): refusal_ok — System prawidłowo odmówił, bo w jego kontekście faktycznie nie było art. 113 ani żadnej informacji o limicie zwolnienia podmiotowego z VAT - przepisy dotyczyły zupełnie innych zwolnień.
**Sędzia 2** (gpt-5.6-terra): partial — Prawidłowo wskazano, że przekazane przepisy nie określają limitu na 2028 r. Pominięto jednak wymagane podanie stanu prawnego na datę korpusu oraz obowiązującego w nim limitu 240 000 zł.

## hybrid/verify=off · g-ooc-17 (out_of_corpus, oczekiwane: provisions_without_verdict)
**Pytanie:** Czy mój jednoosobowy biznes (sprzedaż online, obrót 180 000 zł w tym roku) musi już zarejestrować się jako podatnik VAT?
**Wzorzec:** Mogę przytoczyć przepisy, które regulują tę kwestię: VAT art. 113 ust. 1 zwalnia od podatku sprzedaż, której wartość nie przekroczyła w poprzednim ani bieżącym roku podatkowym 240 000 zł, a VAT art. 113 ust. 5 wskazuje, że zwolnienie traci moc od czynności, którą limit został przekroczony — obowiązek rejestracji wynika z VAT art. 96 ust. 1. Przy obrocie 180 000 zł limit nie został jeszcze przekroczony, ale nie znam szczegółów Pana działalności (np. czy sprzedaje Pan towary/usługi wyłączone z tego zwolnienia na podstawie art. 113 ust. 13, ani jak liczony jest rok podatkowy w Pana przypadku), więc nie mogę rozstrzygnąć ostatecznie, czy obowiązek rejestracji już powstał. To nie jest porada podatkowa; w razie wątpliwości proponuję konsultację z doradcą podatkowym lub wniosek o interpretację indywidualną.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 113 ust. 1): Na podstawie podanych przepisów sprzedaż nie musi być objęta rejestracją jako podatnik VAT czynny, jeżeli masz siedzibę działalności w Polsce, a wartość sprzedaży bez VAT nie przekroczyła 240 000 zł zarówno w poprzednim, jak i bieżącym roku podatkowym. Obrót 180 000 zł w bieżącym roku sam w sobie nie przekracza tego limitu. Nie da się jednak rozstrzygnąć ostatecznie bez informacji o obrocie w poprzednim roku i siedzibie działalności; przepisy nie wskazują szczególnych zasad dla sprzedaży online.
**Kontekst:** VAT art. 96 ust. 4b, VAT art. 96 ust. 10c, VAT art. 96 ust. 10, VAT art. 113 ust. 1, VAT art. 96 ust. 9g
**Sędzia 1** (claude-sonnet-5): partial — Trafnie wskazuje art. 113 ust. 1 i brak przekroczenia limitu 180 000 zł, ale pomija obowiązek rejestracji z art. 96 ust. 1 oraz wyłączenia z art. 113 ust. 13, a stwierdzenie 'przepisy nie wskazują szczególnych zasad dla sprzedaży online' jest dopowiedzeniem spoza kontekstu (art. 96 ust. 1 i ust. 13 nie były nawet przytoczone w kontekście systemu).
**Sędzia 2** (): error — 

## hybrid/verify=off · g-ooc-18 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy od sprzedaży laptopa prywatnie (jako osoba fizyczna, nieprowadząca działalności) muszę zapłacić VAT i jak długo trzeba przechowywać taką transakcję w ewidencji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 15 ust. 1 wskazuje, że podatnikami VAT są podmioty wykonujące samodzielnie działalność gospodarczą — skoro sprzedaje Pan prywatny przedmiot poza taką działalnością, nie jest Pan podatnikiem VAT z tego tytułu, więc VAT nie wystąpi. Natomiast szczegółowe zasady przechowywania ewidencji/dokumentów przez osoby prywatne nieprowadzące działalności nie są uregulowane w ustawie o VAT (ta reguluje obowiązki podatników VAT, a Pan nim nie jest w tej transakcji) — to wykracza poza mój korpus i nie mogę podać odpowiedzi w tej części.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 111 ust. 1, VAT art. 138h): W przepisach, które mam, nie ma odpowiedzi, czy sprzedaż laptopa prywatnie przez osobę fizyczną nieprowadzącą działalności podlega VAT. Nie ma w nich także przepisu określającego, jak długo należy przechowywać ewidencję takiej zwykłej sprzedaży; VAT art. 138h dotyczy ewidencji transakcji objętych procedurą importu, a VAT art. 111 ust. 1 dotyczy ewidencji sprzedaży przy zastosowaniu kas rejestrujących przez podatników. 
**Kontekst:** VAT art. 111 ust. 1, VAT art. 138h, VAT art. 110, VAT art. 138i, VAT art. 111 ust. 3a pkt 1–11, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): partial — System błędnie odmówił odpowiedzi na część dotyczącą VAT, choć art. 15 ust. 1 (jeśli byłby w kontekście) daje jasną odpowiedź – tu jednak art. 15 nie jest w podanych przepisach, więc odmowa w tej części jest w zasadzie uzasadniona na bazie dostępnego kontekstu, ale system nie wskazał wprost, że brak definicji podatnika uniemożliwia odpowiedź, tylko ogólnie stwierdził brak przepisu; część o ewidencji jest poprawnie i wiernie odmówiona z trafnym wskazaniem nieadekwatności art. 111 i 138h.
**Sędzia 2** (): error — 

## hybrid/verify=off · g-ooc-19 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy odsetki za zwłokę w podatku są wysokie i czy mogę zapłacić je kartą płatniczą w urzędzie?
**Wzorzec:** Stawka odsetek za zwłokę to suma 200% podstawowej stopy kredytu lombardowego NBP i 2%, nie mniej niż 8% (Ordynacja art. 56 § 1). Co do zapłaty kartą: Ordynacja dopuszcza zapłatę „innym instrumentem płatniczym” za pośrednictwem konta w e-Urzędzie Skarbowym (art. 61 § 1 pkt 2); zasad płacenia kartą bezpośrednio w kasie urzędu w korpusie nie ma.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 53 § 1, Ordynacja art. 55 § 1, Ordynacja art. 56b): Z podanych przepisów nie wynika konkretna wysokość zwykłych odsetek, więc nie można ocenić, czy są „wysokie”; wynika jedynie, że od zaległości podatkowych nalicza się odsetki za zwłokę, a podatnik wpłaca je bez wezwania organu podatkowego (Ordynacja art. 53 § 1, Ordynacja art. 55 § 1). W podatku od towarów i usług oraz podatku akcyzowym może mieć zastosowanie podwyższona stawka odsetek w wysokości 150% stawki odsetek za zwłokę, jeżeli zachodzą warunki określone w przepisie, w tym dotyczące zaniżenia lub zawyżenia przekraczającego wskazane w nim progi (Ordynacja art. 56b). W podanych przepisach nie ma odpowiedzi, czy odsetki można zapłacić kartą płatniczą w urzędzie.
**Kontekst:** Ordynacja art. 76, Ordynacja art. 53, Ordynacja art. 55, Ordynacja art. 56b
**Sędzia 1** (claude-sonnet-5): partial — System trafnie stwierdza, że w podanym kontekście nie ma stawki podstawowej odsetek (art. 56 §1 nie został mu dostarczony) i prawidłowo odmawia odpowiedzi co do karty płatniczej, ale brak przepisu o podstawowej stawce 8%/200%+2% to ograniczenie kontekstu, nie błąd systemu - odpowiedź jest wewnętrznie poprawna i wiernie oddaje to, czego w kontekście nie ma, jednak nie podaje żadnej konkretnej wartości procentowej, którą wzorzec uznaje za kluczową informację.
**Sędzia 2** (): error — 

## hybrid/verify=off · g-ooc-20 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Sprzedaję używany budynek biurowy, który był zasiedlony 5 lat temu — czy ta dostawa jest zwolniona z VAT, i jaką stawkę PCC zapłaci kupujący od tej transakcji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 43 ust. 1 pkt 10 zwalnia od podatku dostawę budynków, budowli lub ich części, z wyjątkiem dostawy w ramach pierwszego zasiedlenia lub przed nim, oraz dostawy dokonanej w ciągu 2 lat od pierwszego zasiedlenia. Skoro budynek był zasiedlony 5 lat temu (czyli upłynęły więcej niż 2 lata), dostawa korzysta ze zwolnienia z VAT na podstawie tego przepisu. Natomiast kwestia podatku od czynności cywilnoprawnych (PCC), który może obciążać kupującego przy zakupie nieruchomości zwolnionej z VAT, nie jest uregulowana w ustawie o VAT — reguluje ją ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu, więc nie mogę podać stawki PCC.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 43 ust. 10, VAT art. 43 ust. 11): Na podstawie podanych przepisów nie można ustalić, czy dostawa budynku jest zwolniona z VAT, ponieważ nie zawierają one przepisu określającego to zwolnienie ani definicji zasiedlenia. Można jedynie stwierdzić, że podatnik może zrezygnować ze zwolnienia dotyczącego dostawy budynku i wybrać opodatkowanie, jeżeli sprzedawca i nabywca są zarejestrowani jako podatnicy VAT czynni oraz złożą wymagane oświadczenie (VAT art. 43 ust. 10–11). Podane przepisy nie określają stawki PCC od tej transakcji; odpowiedzi należy szukać w ustawie o podatku od czynności cywilnoprawnych.
**Kontekst:** VAT art. 43 ust. 10, VAT art. 29a ust. 8–9, VAT art. 43 ust. 11, VAT art. 120 ust. 13, VAT art. 42 ust. 1
**Sędzia 1** (claude-sonnet-5): incorrect — System błędnie stwierdził, że kontekst nie zawiera podstawy zwolnienia, mimo że art. 43 ust. 1 pkt 10 (kluczowy przepis) nie jest tu wymieniony w dostarczonych przepisach – ale skoro wzorzec zakłada, że ten przepis jest w korpusie, system powinien go znaleźć i zastosować; zamiast tego odmówił odpowiedzi na część, która powinna być możliwa do udzielenia, co jest niezgodne z wzorcem merytorycznie (teza sprzeczna - brak zwolnienia zamiast jego potwierdzenia).
**Sędzia 2** (): error — 

## hybrid/verify=off · g-op-12 (multi, oczekiwane: answer)
**Pytanie:** Złożyłem korektę deklaracji i zapłaciłem zaległość, ale dopiero po tym, jak dostałem zawiadomienie o zamiarze wszczęcia kontroli. Czy przysługuje mi obniżona stawka odsetek za zwłokę?
**Wzorzec:** Nie. Obniżona stawka odsetek (50% stawki odsetek za zwłokę) przysługuje przy korekcie złożonej w ciągu 6 miesięcy od terminu złożenia deklaracji i zapłacie zaległości w ciągu 7 dni od korekty (art. 56a § 1), ale nie stosuje się jej do korekty złożonej po doręczeniu zawiadomienia o zamiarze wszczęcia kontroli podatkowej (art. 56a § 3 pkt 1).
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 56a § 1 pkt 1–2, Ordynacja art. 56a § 3 pkt 1): Nie. Obniżonej stawki odsetek za zwłokę nie stosuje się do korekty deklaracji złożonej po doręczeniu zawiadomienia o zamiarze wszczęcia kontroli podatkowej, niezależnie od tego, że zaległość została zapłacona. Wynik może być inny tylko wtedy, gdy zawiadomienie nie zostało doręczone przed korektą albo zachodzi inna przesłanka dotycząca kontroli wskazana w przepisach; na podstawie podanych faktów obniżona stawka nie przysługuje.
**Kontekst:** Ordynacja art. 56a, Ordynacja art. 56b, Ordynacja art. 57, Ordynacja art. 54
**Sędzia 1** (claude-sonnet-5): correct — System prawidłowo wskazuje odmowę obniżonej stawki z powodu doręczenia zawiadomienia o kontroli, zgodnie z art. 56a § 3 pkt 1, i trafnie podaje negatywną konkluzję; nie myli faktów, choć nie przytacza wprost warunków z § 1 tak dokładnie jak wzorzec.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-01 (fact, oczekiwane: answer)
**Pytanie:** Jaka jest obowiązująca podstawowa stawka podatku VAT?
**Wzorzec:** Obowiązująca podstawowa stawka VAT wynosi 23%. Wynika to z art. 146ef ust. 1 pkt 1, który czasowo podwyższa stawkę podstawową wskazaną w art. 41 ust. 1 (gdzie formalnie zapisano 22%) do 23%, dopóki trwa okres określony w tym przepisie.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 146ef ust. 1 pkt 1): Obowiązująca podstawowa stawka podatku VAT wynosi 23% — jest to stawka wskazana dla art. 41 ust. 1 w VAT art. 146ef ust. 1 pkt 1.
**Kontekst:** VAT art. 146eg, VAT art. 41 ust. 3–4, VAT art. 85, VAT art. 41 ust. 14g, VAT art. 41 ust. 16, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź prawidłowo wskazuje 23% i opiera się na art. 146ef ust. 1 pkt 1 z kontekstu, zgodnie z wzorcem; drobny skrót sformułowania nie zmienia sensu i nie dodaje treści poza przepisami.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-02 (fact, oczekiwane: answer)
**Pytanie:** Od jakiej kwoty faktury za towary z załącznika nr 15 do ustawy podatnik jest obowiązany zastosować mechanizm podzielonej płatności (split payment)?
**Wzorzec:** Przy płatności za towary lub usługi z załącznika nr 15 do ustawy, udokumentowanej fakturą, w której kwota należności ogółem przekracza 15 000 zł (lub równowartość w walucie obcej), podatnik jest obowiązany zastosować mechanizm podzielonej płatności.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 108a ust. 1a): Podatnik jest obowiązany zastosować mechanizm podzielonej płatności przy płatności za towary wymienione w załączniku nr 15, jeżeli kwota należności ogółem na fakturze przekracza 15 000 zł albo równowartość tej kwoty w walucie obcej. Oznacza to, że obowiązek dotyczy faktury powyżej 15 000 zł, a nie faktury na dokładnie 15 000 zł. Kwotę w walucie obcej przelicza się na złote według zasad stosowanych do określenia podstawy opodatkowania.
**Kontekst:** VAT art. 108a ust. 1a, VAT art. 106e ust. 13, VAT art. 108a ust. 7, VAT art. 108a ust. 1, VAT art. 108a ust. 3
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem, prawidłowo podaje próg 15 000 zł i dodatkowo trafnie doprecyzowuje, że obowiązek dotyczy kwot powyżej tego progu, co wynika z art. 108a ust. 1a.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-03 (fact, oczekiwane: answer)
**Pytanie:** Do jakiej kwoty wartości sprzedaży (bez podatku) podatnik może korzystać ze zwolnienia podmiotowego z VAT?
**Wzorzec:** Zwolnienie podmiotowe przysługuje podatnikowi, u którego wartość sprzedaży, bez podatku, nie przekroczyła w poprzednim ani bieżącym roku podatkowym kwoty 240 000 zł.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 113 ust. 1, VAT art. 113 ust. 10): Podatnik posiadający siedzibę działalności gospodarczej na terytorium kraju może korzystać ze zwolnienia podmiotowego z VAT, jeżeli wartość sprzedaży bez podatku nie przekroczyła w poprzednim ani bieżącym roku podatkowym 240 000 zł (VAT art. 113 ust. 1). Jeżeli działalność rozpoczęto w trakcie roku, limit stosuje się proporcjonalnie do okresu prowadzenia działalności, a zwolnienie traci moc od czynności, którą przekroczono ten limit (VAT art. 113 ust. 10).
**Kontekst:** VAT art. 113 ust. 1, VAT art. 113 ust. 10, VAT art. 113a, PIT art. 44 ust. 7c
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem (240 000 zł, art. 113 ust. 1) i poprawnie dodaje istotną informację o proporcjonalnym limicie i utracie zwolnienia z art. 113 ust. 10, co jest wiernym rozszerzeniem opartym na kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-04 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie podatnik powinien wystawić fakturę VAT po dokonaniu dostawy towaru lub wykonaniu usługi?
**Wzorzec:** Fakturę należy wystawić nie później niż 15. dnia miesiąca następującego po miesiącu, w którym dokonano dostawy towaru lub wykonano usługę, z zastrzeżeniem wyjątków z ust. 2–9 art. 106i.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 106i ust. 1, VAT art. 106i ust. 2–9): Podatnik powinien wystawić fakturę nie później niż 15. dnia miesiąca następującego po miesiącu, w którym dokonano dostawy towaru lub wykonano usługę. Termin ten ma zastosowanie z zastrzeżeniem szczególnych terminów określonych w art. 106i ust. 2–9, zależnych m.in. od rodzaju czynności lub otrzymania zapłaty przed dostawą albo wykonaniem usługi.
**Kontekst:** VAT art. 106i, VAT art. 106b, VAT art. 20, VAT art. 103 ust. 5ac
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje termin 15. dnia miesiąca następującego po miesiącu dostawy/usługi oraz zastrzeżenie wyjątków z ust. 2-9, zgodnie z art. 106i ust. 1.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-05 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie podatnik VAT rozliczający się miesięcznie musi wpłacić podatek na rachunek urzędu skarbowego?
**Wzorzec:** Podatnicy są obowiązani, bez wezwania naczelnika urzędu skarbowego, wpłacać podatek za okresy miesięczne w terminie do 25. dnia miesiąca następującego po miesiącu, w którym powstał obowiązek podatkowy.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 103 ust. 1): Podatnik VAT rozliczający się miesięcznie musi obliczyć i wpłacić podatek na rachunek urzędu skarbowego bez wezwania, do 25. dnia miesiąca następującego po miesiącu, w którym powstał obowiązek podatkowy. Dotyczy to zasad ogólnych, z zastrzeżeniem wyjątków wskazanych w przepisie.
**Kontekst:** VAT art. 103 ust. 1, VAT art. 103 ust. 2, PIT art. 44 ust. 1f, VAT art. 99 ust. 11a, PIT art. 30g ust. 11
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje termin 25. dnia miesiąca następującego, zgodnie z art. 103 ust. 1, i słusznie zaznacza zastrzeżenia/wyjątki wskazane w przepisie, nie dodając informacji spoza kontekstu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-06 (fact, oczekiwane: answer)
**Pytanie:** Po ilu dniach od terminu płatności można uznać nieściągalność wierzytelności za uprawdopodobnioną na potrzeby ulgi na złe długi?
**Wzorzec:** Nieściągalność wierzytelności uważa się za uprawdopodobnioną, gdy wierzytelność nie została uregulowana lub zbyta w jakiejkolwiek formie w ciągu 90 dni od dnia upływu terminu jej płatności określonego w umowie lub na fakturze.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 89a ust. 1a): Nieściągalność wierzytelności uznaje się za uprawdopodobnioną po 90 dniach od upływu terminu jej płatności określonego w umowie lub na fakturze, jeżeli wierzytelność nie została w tym czasie uregulowana ani zbyta. (VAT art. 89a ust. 1a)
**Kontekst:** VAT art. 89a, VAT art. 89b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź wiernie oddaje treść art. 89a ust. 1a – 90 dni od terminu płatności, brak uregulowania/zbycia wierzytelności, poprawny cytat przepisu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-07 (fact, oczekiwane: answer)
**Pytanie:** Jaki procent VAT z faktury za wydatki związane z samochodem osobowym używanym zarówno w firmie, jak i prywatnie można co do zasady odliczyć?
**Wzorzec:** Co do zasady, w przypadku wydatków związanych z pojazdami samochodowymi, kwotę podatku naliczonego stanowi 50% kwoty podatku wynikającej z faktury (lub należnego w przypadkach wymienionych w art. 86a ust. 1).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 86a ust. 2, VAT art. 86a ust. 4, VAT art. 86a ust. 5): W podanych przepisach nie ma wartości procentowej odliczenia VAT dla samochodu osobowego używanego zarówno firmowo, jak i prywatnie. Przepisy wskazują, że wydatki obejmują m.in. nabycie, używanie, paliwo, naprawy i eksploatację pojazdu (VAT art. 86a ust. 2), a pełne wykorzystanie wyłącznie do działalności wymaga spełnienia warunków określonych w VAT art. 86a ust. 4; nie wynika z nich jednak konkretny procent odliczenia dla użytku mieszanego.
**Kontekst:** VAT art. 86a ust. 11, PIT art. 23 ust. 1 pkt 45c–47, VAT art. 86a ust. 2, VAT art. 86a ust. 4, VAT art. 86a ust. 5
**Sędzia 1** (claude-sonnet-5): incorrect — System błędnie stwierdził, że w kontekście nie ma informacji o procencie odliczenia VAT, podczas gdy art. 86a ust. 1 (choć nie podany w kontekście systemu) jest wzorcową podstawą 50%; system nie znalazł odpowiedzi mimo że pytanie dotyczyło faktów, które powinny być dostępne – to odmowa, gdzie odpowiedź była możliwa (w pełnym kontekście ustawy), więc powinien być refusal_missing, ale biorąc pod uwagę, że system faktycznie nie miał w swoim kontekście ust. 1, jego odmowa jest zgodna z tym, co dostał, jednak względem wzorca (pytanie wymagało znanej stawki 50%) odpowiedź jest błędna/niekompletna co do głównej tezy.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-08 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie urząd skarbowy powinien zwrócić podatnikowi różnicę podatku VAT (nadwyżkę podatku naliczonego nad należnym) na rachunek bankowy?
**Wzorzec:** Zwrot różnicy podatku następuje w terminie 40 dni od dnia złożenia rozliczenia przez podatnika, z zastrzeżeniem wyjątków wskazanych w ust. 6, 6a i 6d art. 87.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 87 ust. 2, VAT art. 87 ust. 6 pkt 1–3, VAT art. 87 ust. 6d, VAT art. 87 ust. 5a): Co do zasady zwrot różnicy podatku VAT na rachunek bankowy następuje w terminie 40 dni od dnia złożenia rozliczenia (VAT art. 87 ust. 2). Termin wynosi 25 dni, jeżeli łącznie spełnione są warunki określone w VAT art. 87 ust. 6 pkt 1–3. Termin 15 dni ma zastosowanie w przypadkach wskazanych w VAT art. 87 ust. 6d, natomiast gdy podatnik nie wykonał w okresie rozliczeniowym czynności opodatkowanych na terytorium kraju ani czynności wymienionych w VAT art. 86 ust. 8 pkt 1, termin wynosi 180 dni, a po złożeniu zabezpieczenia majątkowego może wynosić 60 dni (VAT art. 87 ust. 5a). Ostateczny termin zależy więc od spełnienia warunków właściwego trybu zwrotu.
**Kontekst:** VAT art. 87 ust. 2, VAT art. 87 ust. 6 pkt 1–3, VAT art. 87 ust. 6a, VAT art. 87 ust. 6d, VAT art. 87 ust. 5a
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie podaje podstawowy termin 40 dni (art. 87 ust. 2) i trafnie uzupełnia go wyjątkami (25, 15, 180, 60 dni) z art. 87 ust. 6, 6d i 5a, które są dokładnie tymi zastrzeżeniami, do których odwołuje się wzorzec. Wszystkie twierdzenia wynikają bezpośrednio z przytoczonych przepisów w kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-09 (fact, oczekiwane: answer)
**Pytanie:** Jak długo podatnik musi przechowywać ewidencje i faktury związane z rozliczaniem VAT?
**Wzorzec:** Podatnicy są obowiązani przechowywać ewidencje oraz wszystkie dokumenty, w szczególności faktury, związane z rozliczaniem VAT do czasu upływu terminu przedawnienia zobowiązania podatkowego (z zastrzeżeniami wymienionymi w art. 112).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 112, VAT art. 112a ust. 1, VAT art. 112aa ust. 1–2): Podatnik musi przechowywać ewidencje i wszystkie dokumenty, w szczególności faktury, związane z rozliczaniem VAT do upływu terminu przedawnienia zobowiązania podatkowego (VAT art. 112). Faktury należy przechowywać w sposób zapewniający ich łatwe odszukanie, autentyczność pochodzenia, integralność treści i czytelność do tego samego momentu (VAT art. 112a ust. 1). Wyjątkiem są faktury przechowywane w Krajowym Systemie e-Faktur, które są przechowywane przez 10 lat od końca roku ich wystawienia; jeżeli ten okres upłynie przed terminem przedawnienia, podatnik przechowuje je poza systemem do upływu tego terminu (VAT art. 112aa ust. 1–2).
**Kontekst:** VAT art. 112, VAT art. 112a, VAT art. 109b, VAT art. 112aa, VAT art. 116 ust. 10
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje główną zasadę (przechowywanie do upływu terminu przedawnienia) i trafnie uzupełnia ją o szczegóły z art. 112a i 112aa dotyczące faktur, w tym wyjątek KSeF (10 lat), co jest zgodne z kontekstem i nie zmienia sensu wzorca.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-10 (fact, oczekiwane: answer)
**Pytanie:** W którym momencie co do zasady powstaje obowiązek podatkowy w VAT?
**Wzorzec:** Obowiązek podatkowy powstaje z chwilą dokonania dostawy towarów lub wykonania usługi, z zastrzeżeniem wyjątków wskazanych w ust. 1a, 1b, 5 i 7–11 oraz innych wskazanych przepisów.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 19a ust. 1, VAT art. 19a ust. 8, VAT art. 19a ust. 5 pkt 1–2, VAT art. 21 ust. 1 i 6): Co do zasady obowiązek podatkowy w VAT powstaje z chwilą dokonania dostawy towarów lub wykonania usługi (VAT art. 19a ust. 1). Jeżeli przed dostawą lub wykonaniem usługi otrzymano całość albo część zapłaty, obowiązek co do zasady powstaje z chwilą jej otrzymania, w odniesieniu do otrzymanej kwoty (VAT art. 19a ust. 8). Od tych zasad przewidziano wyjątki, w tym dotyczące niektórych dostaw, usług, dotacji oraz podatników stosujących metodę kasową (VAT art. 19a ust. 1, VAT art. 19a ust. 5 pkt 1–2, VAT art. 21 ust. 1 i 6).
**Kontekst:** VAT art. 19a ust. 1, VAT art. 19a ust. 1b, VAT art. 19a ust. 8, VAT art. 19a ust. 5 pkt 1–2, VAT art. 21
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź prawidłowo wskazuje zasadę ogólną (art. 19a ust. 1) oraz wymienia kluczowe wyjątki (zaliczki, dotacje, metoda kasowa) zgodnie z przepisami w kontekście, nie wprowadzając treści spoza podanych artykułów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-11 (fact, oczekiwane: answer)
**Pytanie:** Jaka stawka VAT obowiązuje obecnie dla towarów i usług wymienionych w załączniku nr 10 do ustawy (np. podstawowe produkty spożywcze)?
**Wzorzec:** Dla towarów i usług z załącznika nr 10 (innych niż PKWiU 56 – wyżywienie) obowiązuje stawka 5% zgodnie z art. 41 ust. 2a.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 41 ust. 2a, VAT art. 146ef ust. 1 pkt 2): Obecnie stawka VAT wynosi 5% dla towarów i usług wymienionych w załączniku nr 10 do ustawy, jeżeli nie są klasyfikowane jako usługi związane z wyżywieniem (PKWiU 56), zgodnie z VAT art. 41 ust. 2a. Dotyczy to przykładowo podstawowych produktów spożywczych objętych załącznikiem nr 10. Przepis przejściowy VAT art. 146ef zastępuje obecnie stawkę z VAT art. 41 ust. 2 stawką 8%, ale nie zmienia stawki 5% określonej w VAT art. 41 ust. 2a.
**Kontekst:** VAT art. 41 ust. 12f, VAT art. 41 ust. 2a, VAT art. 41 ust. 2, VAT art. 83 ust. 13, VAT art. 85, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź prawidłowo wskazuje stawkę 5% z art. 41 ust. 2a dla załącznika nr 10 (z wyłączeniem PKWiU 56) i zgodnie z kontekstem zauważa, że art. 146ef dotyczy jedynie podmiany stawki z art. 41 ust. 2 (na 8%), nie wpływając na stawkę 5% z ust. 2a.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-12 (fact, oczekiwane: answer)
**Pytanie:** Czy usługi w zakresie opieki medycznej wykonywane w ramach działalności leczniczej przez podmioty lecznicze są objęte VAT?
**Wzorzec:** Nie — usługi w zakresie opieki medycznej służące profilaktyce, zachowaniu, ratowaniu, przywracaniu i poprawie zdrowia, wykonywane w ramach działalności leczniczej przez podmioty lecznicze, są zwolnione od podatku VAT.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 43 ust. 1 pkt 18): Usługi w zakresie opieki medycznej służące profilaktyce, zachowaniu, ratowaniu, przywracaniu i poprawie zdrowia, wykonywane w ramach działalności leczniczej przez podmioty lecznicze, są zwolnione od VAT. Zwolnienie obejmuje także dostawę towarów i świadczenie usług ściśle związane z tymi usługami. Wynik zależy od spełnienia wskazanego celu medycznego oraz wykonywania usług przez podmiot leczniczy w ramach działalności leczniczej.
**Kontekst:** VAT art. 43 ust. 1 pkt 14–18a, VAT art. 43 ust. 1 pkt 19–21, VAT art. 43 ust. 1 pkt 22–25, VAT art. 145d, VAT art. 43 ust. 1 pkt 37–41
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź wiernie odwzorowuje art. 43 ust. 1 pkt 18, poprawnie wskazując zwolnienie z VAT oraz warunki (cel medyczny, podmiot leczniczy, działalność lecznicza), bez błędów i dopowiedzeń spoza kontekstu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-13 (multi, oczekiwane: answer)
**Pytanie:** Spółka A i spółka B należą do tej samej grupy VAT. Czy sprzedaż towarów między nimi podlega opodatkowaniu VAT?
**Wzorzec:** Nie — dostawa towarów i świadczenie usług dokonane przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlegają opodatkowaniu (art. 8c ust. 1), o ile spółki A i B tworzą grupę VAT w rozumieniu art. 2 pkt 47, czyli grupę podmiotów powiązanych finansowo, ekonomicznie i organizacyjnie, zarejestrowaną jako podatnik podatku.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 8c ust. 1): Nie. Dostawa towarów dokonana przez członka grupy VAT na rzecz innego członka tej samej grupy VAT nie podlega opodatkowaniu VAT (VAT art. 8c ust. 1).
**Kontekst:** VAT art. 8c
**Sędzia 1** (claude-sonnet-5): partial — Poprawnie wskazuje art. 8c ust. 1 i brak opodatkowania, ale pomija świadczenie usług oraz warunek, że A i B muszą faktycznie tworzyć grupę VAT w rozumieniu art. 2 pkt 47 (co wzorzec zaznacza).
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje, że dostawa towarów między członkami tej samej grupy VAT nie podlega opodatkowaniu, zgodnie z art. 8c ust. 1 ustawy o VAT.

## hyde/verify=off · g-vat-14 (multi, oczekiwane: answer)
**Pytanie:** Jestem małym podatnikiem VAT (w rozumieniu art. 2 pkt 25) i wybrałem metodę kasową rozliczeń. Jak często składam deklaracje podatkowe?
**Wzorzec:** Jako mały podatnik, który wybrał metodę kasową, składa Pan deklaracje podatkowe w urzędzie skarbowym za okresy kwartalne, w terminie do 25. dnia miesiąca następującego po każdym kolejnym kwartale — status małego podatnika wymaga, aby wartość sprzedaży (wraz z podatkiem) nie przekroczyła w poprzednim roku podatkowym równowartości 2 000 000 euro.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 99 ust. 2, VAT art. 21 ust. 4): Składasz deklaracje podatkowe za okresy kwartalne, w terminie do 25. dnia miesiąca następującego po każdym kolejnym kwartale. Dotyczy to małego podatnika, który wybrał metodę kasową; przepisy przewidują jednak utratę prawa do metody kasowej od rozliczenia za miesiąc następujący po kwartale, w którym przekroczono kwotę określoną w art. 2 pkt 25.
**Kontekst:** VAT art. 99 ust. 2, VAT art. 99 ust. 5, VAT art. 99 ust. 3, VAT art. 99 ust. 1, VAT art. 21
**Sędzia 1** (claude-sonnet-5): correct — Główna teza (kwartalne deklaracje do 25. dnia miesiąca po kwartale) jest zgodna z wzorcem, dodatkowo system poprawnie wspomina o utracie prawa do metody kasowej przy przekroczeniu limitu, co jest trafnym uzupełnieniem opartym na art. 21 ust. 4. Brak jedynie wprost podanej kwoty 2 000 000 euro, ale to nie zmienia poprawności głównej odpowiedzi.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-15 (multi, oczekiwane: answer)
**Pytanie:** Prowadzę działalność jako mały podatnik i wybrałem metodę kasową — kiedy powstaje u mnie obowiązek podatkowy, jeśli sprzedaję towar osobie fizycznej nieprowadzącej działalności gospodarczej (czyli podmiotowi innemu niż czynny podatnik VAT z art. 15)?
**Wzorzec:** Obowiązek podatkowy powstaje z dniem otrzymania całości lub części zapłaty, jednak nie później niż 180. dnia, licząc od dnia wydania towaru lub wykonania usługi — zgodnie z art. 21 ust. 1 pkt 2, który stosuje się do dostaw na rzecz podmiotów innych niż zarejestrowani podatnicy VAT czynni z art. 15.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 21 ust. 1 pkt 2, VAT art. 21 ust. 2): Obowiązek podatkowy powstaje z dniem otrzymania całości lub części zapłaty, przy czym nie później niż 180. dnia, licząc od dnia wydania towaru. Otrzymanie części zapłaty powoduje powstanie obowiązku podatkowego w tej części. Zasada ta dotyczy czynności wykonanych w okresie stosowania metody kasowej.
**Kontekst:** VAT art. 21, VAT art. 20, VAT art. 106ga
**Sędzia 1** (claude-sonnet-5): correct — Poprawnie wskazano art. 21 ust. 1 pkt 2 (zapłata/180 dni) i art. 21 ust. 2 (dotyczy czynności z okresu stosowania metody kasowej); choć nie zacytowano literalnie warunku 'podmiot inny niż z art. 15', treść odpowiedzi jest zgodna z wzorcem i wynika z przepisów w kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-16 (multi, oczekiwane: answer)
**Pytanie:** Czy podatnik prowadzący kancelarię prawniczą o rocznej sprzedaży 100 000 zł może skorzystać ze zwolnienia podmiotowego z VAT z art. 113?
**Wzorzec:** Nie. Mimo że wartość sprzedaży (100 000 zł) nie przekracza limitu 240 000 zł z art. 113 ust. 1, zwolnień z ust. 1 i 9 nie stosuje się do podatników świadczących usługi prawnicze — wyłączenie to wynika wprost z art. 113 ust. 13 pkt 2 lit. a.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 113 ust. 1, VAT art. 113a ust. 1 pkt 3): Na podstawie podanych przepisów nie można rozstrzygnąć, czy kancelaria prawna może skorzystać ze zwolnienia, ponieważ art. 113 ust. 1 wymaga, aby podatnik z siedzibą działalności w kraju nie przekroczył kwoty 240 000 zł zarówno w poprzednim, jak i bieżącym roku podatkowym. Sprzedaż 100 000 zł spełnia ten warunek kwotowy, ale brakuje przepisu art. 113 ust. 13, do którego należy sprawdzić, czy wykonywane usługi nie są wyłączone ze zwolnienia. W przepisach, które mam, nie ma treści art. 113 ust. 13, więc nie mogę potwierdzić prawa kancelarii prawnej do zwolnienia.
**Kontekst:** VAT art. 113 ust. 1, VAT art. 113a, VAT art. 43 ust. 22, VAT art. 14 ust. 2, VAT art. 84
**Sędzia 1** (claude-sonnet-5): refusal_missing — System prawidłowo zauważył brak treści art. 113 ust. 13 w kontekście i nie zmyślił wyłączenia dla usług prawniczych, ale zgodnie z zasadami oceny odmowa tam, gdzie oczekiwano odpowiedzi merytorycznej na podstawie przepisów, liczy się jako refusal_missing – choć w tym przypadku odmowa była uczciwa, bo kluczowy przepis faktycznie nie znalazł się w kontekście systemu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-17 (multi, oczekiwane: answer)
**Pytanie:** Czy wewnątrzwspólnotowa dostawa towarów (WDT) jest zawsze opodatkowana stawką 0%?
**Wzorzec:** Nie zawsze — art. 41 ust. 3 przewiduje stawkę 0% dla WDT, ale z zastrzeżeniem art. 42, który uzależnia zastosowanie tej stawki od spełnienia warunków: dostawy na rzecz nabywcy z ważnym numerem VAT-UE, posiadania dowodów wywozu towarów do innego państwa członkowskiego oraz bycia zarejestrowanym jako podatnik VAT UE przy składaniu deklaracji.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 41 ust. 3, VAT art. 42 ust. 1): Nie. WDT podlega stawce 0% tylko pod warunkiem spełnienia wymogów z VAT art. 42 ust. 1: nabywca musi mieć właściwy i ważny numer identyfikacyjny VAT UE, podatnik musi posiadać dowody wywozu i dostarczenia towarów do innego państwa członkowskiego przed terminem złożenia deklaracji oraz być zarejestrowany jako podatnik VAT UE. VAT art. 41 ust. 3 stanowi, że stawka 0% w WDT obowiązuje z zastrzeżeniem VAT art. 42.
**Kontekst:** VAT art. 42 ust. 1, VAT art. 41 ust. 3–4, VAT art. 10, VAT art. 83 ust. 11
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje, że stawka 0% wymaga spełnienia warunków z art. 42 ust. 1 (ważny numer VAT-UE, dowody wywozu/dostawy, rejestracja VAT UE) oraz powołuje art. 41 ust. 3, zgodnie z wzorcem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-18 (multi, oczekiwane: answer)
**Pytanie:** Kupiłem w 2023 roku maszynę produkcyjną (środek trwały) za 100 000 zł netto i odliczyłem cały VAT, zakładając wykorzystanie wyłącznie do czynności opodatkowanych. W kolejnych latach część produkcji objęto czynnościami zwolnionymi. Czy muszę korygować odliczony podatek?
**Wzorzec:** Tak. Gdy podatnik odliczył cały VAT, a potem zmieniło się prawo do odliczenia (część wykorzystania to czynności zwolnione), stosuje się odpowiednio przepisy o korekcie (art. 91 ust. 7). Dla środka trwałego o wartości początkowej powyżej 15 000 zł korekty dokonuje się w ciągu 5 kolejnych lat, licząc od roku oddania do użytkowania; roczna korekta dotyczy jednej piątej kwoty podatku naliczonego przy nabyciu (art. 91 ust. 2).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 91 ust. 7a, VAT art. 91 ust. 2): Tak, jeżeli zmiana wykorzystania maszyny do czynności zwolnionych nastąpiła w okresie korekty i zmieniła prawo do odliczenia, należy dokonać korekty odliczonego podatku przy tej zmianie (VAT art. 91 ust. 7a). Ponieważ wartość początkowa maszyny przekracza 15 000 zł, korekta odbywa się przez 5 kolejnych lat, licząc od roku oddania jej do użytkowania, a roczna korekta dotyczy jednej piątej podatku naliczonego przy nabyciu lub wytworzeniu (VAT art. 91 ust. 2). Nie da się określić kwoty korekty na podstawie podanych informacji, ponieważ brakuje kwoty podatku naliczonego, roku oddania maszyny do użytkowania oraz zakresu zmiany wykorzystania do czynności zwolnionych.
**Kontekst:** VAT art. 91 ust. 2, VAT art. 90a, VAT art. 91 ust. 7a, VAT art. 91 ust. 6, VAT art. 91 ust. 1b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem – trafnie wskazuje art. 91 ust. 7a (analogiczny do ust. 7 we wzorcu) oraz zasady z art. 91 ust. 2 dot. 5-letniej korekty i 1/5 kwoty, dodatkowo zasadnie zaznacza brak danych do wyliczenia konkretnej kwoty.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-19 (multi, oczekiwane: answer)
**Pytanie:** Mój klient nie zapłacił mi za fakturę wystawioną 2 lata temu i minęło już 90 dni od terminu płatności. Czy mogę skorygować podatek należny z tytułu tej nieściągalnej wierzytelności?
**Wzorzec:** Tak, co do zasady — nieściągalność uważa się za uprawdopodobnioną po 90 dniach od terminu płatności (art. 89a ust. 1a), a korekta jest możliwa, o ile wierzyciel na dzień poprzedzający złożenie korygującej deklaracji jest zarejestrowanym podatnikiem VAT czynnym oraz od wystawienia faktury nie upłynęły 3 lata, licząc od końca roku, w którym ją wystawiono (art. 89a ust. 2 pkt 3 lit. a i pkt 5). Przy fakturze wystawionej 2 lata temu warunek 3-letni jest jeszcze spełniony.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 89a ust. 1, VAT art. 89a ust. 1a, VAT art. 89a ust. 2 pkt 3 lit. a, VAT art. 89a ust. 2 pkt 5, VAT art. 89a ust. 3, VAT art. 89a ust. 5): Tak, możesz skorygować podstawę opodatkowania i podatek należny, jeżeli nieściągalność wierzytelności została uprawdopodobniona, czyli wierzytelność nie została uregulowana ani zbyta w ciągu 90 dni od upływu terminu płatności. Korekta może nastąpić w rozliczeniu za okres, w którym upłynęło te 90 dni, pod warunkiem że do dnia złożenia deklaracji wierzytelność nadal nie została uregulowana ani zbyta. Musisz również być podatnikiem zarejestrowanym jako podatnik VAT czynny na dzień poprzedzający złożenie deklaracji, a od wystawienia faktury nie mogą upłynąć 3 lata, licząc od końca roku jej wystawienia; w deklaracji należy poinformować właściwego naczelnika urzędu skarbowego o korekcie. Na podstawie podanych informacji nie da się potwierdzić spełnienia wszystkich tych warunków, w szczególności Twojego statusu VAT czynnego i tego, czy wierzytelność nie została zbyta.
**Kontekst:** VAT art. 89b, VAT art. 89a, PIT art. 26i ust. 2
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie wskazuje wszystkie istotne warunki (90 dni, brak uregulowania/zbycia, status VAT czynny, limit 3 lat, obowiązek informacyjny) zgodnie z art. 89a, i trafnie zauważa, że status VAT czynny oraz ewentualne zbycie wierzytelności nie zostały podane przez użytkownika - to rozsądne doprecyzowanie, a nie nadmierna odmowa. Wszystkie twierdzenia mają podstawę w cytowanych przepisach.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-20 (multi, oczekiwane: answer)
**Pytanie:** Jestem informatykiem-freelancerem (osoba fizyczna prowadząca jednoosobową działalność, nie spółka) i chcę wystawiać standardowe faktury papierowe moim klientom-firmom bez użycia KSeF — czy to legalne?
**Wzorzec:** Nie — zgodnie z art. 106ga ust. 1 podatnicy są obowiązani wystawiać faktury ustrukturyzowane przy użyciu Krajowego Systemu e-Faktur. Wyjątki od tego obowiązku, określone w art. 106ga ust. 2, dotyczą m.in. podatników bez siedziby w Polsce, sprzedaży na rzecz osób fizycznych nieprowadzących działalności czy korzystających z niektórych procedur szczególnych — żaden z tych wyjątków nie obejmuje zwykłego freelancera fakturującego firmy w Polsce.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 106ga ust. 1–3): Co do zasady nie: podatnicy są obowiązani wystawiać faktury ustrukturyzowane przy użyciu KSeF, a sam fakt, że jesteś osobą fizyczną prowadzącą jednoosobową działalność, nie stanowi wyjątku (VAT art. 106ga ust. 1–2). Papierowe faktury bez KSeF są dopuszczalne, jeżeli zachodzi jeden z wyjątków, w szczególności gdy korzystasz ze zwolnienia, o którym mowa w art. 113a ust. 1, albo wystawiasz fakturę w jednym z pozostałych przypadków wskazanych w VAT art. 106ga ust. 2; wtedy wystawia się faktury elektroniczne lub papierowe (VAT art. 106ga ust. 3). Na podstawie podanych informacji nie da się ustalić, czy któryś z tych wyjątków ma zastosowanie, więc wynik zależy od Twojego statusu i rodzaju dokumentowanych czynności.
**Kontekst:** VAT art. 106gb, VAT art. 106ga, VAT art. 106r, VAT art. 106gba
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź prawidłowo wskazuje zasadę z art. 106ga ust. 1-3, trafnie zauważa że bycie freelancerem JDG nie jest wyjątkiem, i poprawnie wymienia wyjątki (w tym art. 113a ust. 1) jako warunkowe, nie stwierdzając błędnie że freelancer się kwalifikuje — zgodne z wzorcem co do sensu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-21 (colloquial, oczekiwane: answer)
**Pytanie:** Wystawiłem klientowi fakturę, ale pomyliłem się w cenie jednostkowej towaru. Czy mogę po prostu wystawić nową, poprawną fakturę zamiast tej błędnej?
**Wzorzec:** Nie — w przypadku stwierdzenia pomyłki w jakiejkolwiek pozycji faktury podatnik wystawia fakturę korygującą, a nie zwykłą nową fakturę zastępującą poprzednią. Faktura korygująca musi zawierać m.in. numer kolejny, datę wystawienia oraz odniesienie do faktury, której dotyczy.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 106j ust. 1 pkt 5, VAT art. 106j ust. 2 pkt 5–6): Nie — w podanych przepisach pomyłka w cenie jednostkowej jest pomyłką w pozycji faktury, więc należy wystawić fakturę korygującą. Jeżeli korekta wpływa na podstawę opodatkowania lub kwotę podatku należnego, faktura korygująca powinna zawierać odpowiednią kwotę korekty; w innych przypadkach — prawidłową treść korygowanej pozycji. Z podanych przepisów nie wynika możliwość zastąpienia błędnej faktury po prostu nową fakturą.
**Kontekst:** VAT art. 106j, VAT art. 106e ust. 8, VAT art. 29a ust. 14, VAT art. 106nf
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź systemu poprawnie wskazuje konieczność wystawienia faktury korygującej, trafnie wyjaśnia różnicowanie treści korekty wg art. 106j ust. 2 pkt 5-6 i zgodna jest z wzorcem, bez twierdzeń wykraczających poza przytoczone przepisy.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-22 (colloquial, oczekiwane: answer)
**Pytanie:** Mam mały warzywniak i kupiłem nowy samochód osobowy do rozwożenia towaru do klientów, ale czasem jeżdżę nim też prywatnie. Mogę odliczyć cały VAT z faktury za auto?
**Wzorzec:** Nie w pełni — jeśli samochód jest używany również do celów prywatnych (nie wyłącznie do działalności), przysługuje odliczenie tylko 50% kwoty podatku naliczonego z faktury. Pełne odliczenie byłoby możliwe tylko, gdyby pojazd był wykorzystywany wyłącznie do działalności gospodarczej, co trzeba dodatkowo potwierdzić ewidencją przebiegu pojazdu.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 86a ust. 4, VAT art. 86a ust. 9): Z podanych przepisów nie wynika, że możesz odliczyć cały VAT z faktury. Prywatne używanie samochodu oznacza, że jego sposób wykorzystywania co do zasady nie wyklucza użycia do celów niezwiązanych z działalnością, więc nie spełnia warunku z VAT art. 86a ust. 4 pkt 1; wyjątkiem byłaby sytuacja, gdy konstrukcja pojazdu powoduje, że takie użycie jest nieistotne zgodnie z VAT art. 86a ust. 4 pkt 2. Przepisy, które mam, nie określają jednak wysokości odliczenia w przypadku używania mieszanego, dlatego nie mogę rozstrzygnąć, jaką konkretnie część VAT możesz odliczyć.
**Kontekst:** VAT art. 86a ust. 9, VAT art. 86a ust. 4, VAT art. 86a ust. 5, VAT art. 86a ust. 6, VAT art. 86a ust. 12
**Sędzia 1** (claude-sonnet-5): partial — System poprawnie wnioskuje, że pełne odliczenie nie przysługuje, ale odmawia podania kluczowej informacji (50% odliczenia), która w rzeczywistości powinna być znana z art. 86a (choć konkretny ust. o 50% nie został dostarczony w kontekście, więc odmowa jest usprawiedliwiona brakiem przepisu) - mimo to brakuje istotnej części odpowiedzi zawartej we wzorcu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-23 (colloquial, oczekiwane: answer)
**Pytanie:** Prowadzę gabinet dentystyczny — czy muszę doliczać VAT do usług leczenia pacjentów?
**Wzorzec:** Nie. Usługi w zakresie opieki medycznej świadczone w ramach wykonywania zawodu lekarza dentysty, służące profilaktyce, zachowaniu, ratowaniu, przywracaniu i poprawie zdrowia, są zwolnione od podatku VAT.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 43 ust. 1 pkt 19 lit. a): Nie musisz doliczać VAT, jeżeli usługi leczenia pacjentów są usługami opieki medycznej służącymi profilaktyce, zachowaniu, ratowaniu, przywracaniu lub poprawie zdrowia i są świadczone w ramach wykonywania zawodu lekarza dentysty — takie usługi są zwolnione z VAT (VAT art. 43 ust. 1 pkt 19 lit. a). Z podanych przepisów nie wynika jednak, że każda usługa świadczona w gabinecie dentystycznym automatycznie korzysta ze zwolnienia; wynik zależy od charakteru konkretnej usługi i sposobu jej świadczenia.
**Kontekst:** VAT art. 43 ust. 1 pkt 14–18a, VAT art. 43 ust. 1 pkt 19–21, VAT art. 28a, VAT art. 109 ust. 3a, VAT art. 83 ust. 9
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje zwolnienie z art. 43 ust. 1 pkt 19 lit. a dla usług opieki medycznej lekarza dentysty, zgodnie z wzorcem, a dodatkowe zastrzeżenie o zależności od charakteru usługi jest trafną i uzasadnioną w przepisach ostrożnością, nie wprowadza błędu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-24 (colloquial, oczekiwane: answer)
**Pytanie:** Sprzedaję towar w internecie i pobieram od klienta oprócz ceny towaru także osobną opłatę za koszty przesyłki (wysyłkę kurierem). Czy VAT naliczam tylko od ceny towaru, czy też od kosztów wysyłki?
**Wzorzec:** Od obu kwot łącznie — podstawa opodatkowania obejmuje koszty dodatkowe, takie jak koszty transportu, pobierane przez dokonującego dostawy od nabywcy, więc opłata za przesyłkę wchodzi do podstawy opodatkowania VAT na takich samych zasadach jak cena towaru.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 29a ust. 6 pkt 2): Jeżeli pobierasz od klienta opłatę za przesyłkę, podstawa opodatkowania obejmuje także ten koszt, a nie tylko cenę towaru. Koszty transportu pobierane przez dokonującego dostawy od nabywcy są kosztami dodatkowymi objętymi podstawą opodatkowania (VAT art. 29a ust. 6 pkt 2).
**Kontekst:** VAT art. 138a, VAT art. 29a ust. 6, VAT art. 22 ust. 1 pkt 1–4, PIT art. 22g ust. 3, VAT art. 7a
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje, że koszty przesyłki wchodzą do podstawy opodatkowania VAT na podstawie art. 29a ust. 6 pkt 2, zgodnie z wzorcem, bez dodawania treści spoza przepisów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-25 (colloquial, oczekiwane: answer)
**Pytanie:** Otwieram warsztat krawiecki i będę podatnikiem VAT (nie korzystam ze zwolnienia). Czy muszę się zgłosić do urzędu skarbowego przed pierwszą sprzedażą, czy mogę to zrobić później, np. po miesiącu działania?
**Wzorzec:** Musi Pani złożyć naczelnikowi urzędu skarbowego zgłoszenie rejestracyjne przed dniem wykonania pierwszej czynności opodatkowanej (np. pierwszej sprzedaży) — zgłoszenia po fakcie nie przewidziano jako zgodnego z ustawą terminu.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 96 ust. 5 pkt 1, VAT art. 96 ust. 3): Z VAT art. 96 ust. 5 pkt 1 wynika, że podmioty, o których mowa w VAT art. 96 ust. 3, rozpoczynające sprzedaż opodatkowaną muszą złożyć zgłoszenie przed dniem pierwszej sprzedaży, a nie po miesiącu działania. Podane przepisy nie pozwalają jednak ustalić obowiązku rejestracji dla podatnika, który od początku nie korzysta ze zwolnienia, ponieważ nie zawierają treści VAT art. 96 ust. 1 i ust. 3. W tym zakresie brakuje podstawy do pełnej odpowiedzi.
**Kontekst:** VAT art. 96 ust. 5, VAT art. 96 ust. 9h, VAT art. 97 ust. 1, VAT art. 33b, VAT art. 96 ust. 9
**Sędzia 1** (claude-sonnet-5): partial — Główna teza (zgłoszenie przed pierwszą sprzedażą) jest prawidłowo wyprowadzona z art. 96 ust. 5 pkt 1 i zgodna z wzorcem, ale system niepotrzebnie dodaje częściową odmowę, twierdząc że nie może ustalić obowiązku bez ust. 1 i 3 – podczas gdy ust. 5 pkt 1 wprost obejmuje przypadek 'rozpoczęcia sprzedaży opodatkowanej', co w pełni odpowiada sytuacji z pytania; ta nadmierna zastrzeżoność wprowadza niepotrzebną niejasność.
**Sędzia 2** (): error — 

## hyde/verify=off · g-vat-26 (colloquial, oczekiwane: answer)
**Pytanie:** Otworzyłem warsztat samochodowy i sprzedaję usługi naprawy głównie osobom prywatnym za gotówkę. Czy muszę mieć kasę fiskalną?
**Wzorzec:** Tak, co do zasady — podatnicy dokonujący sprzedaży na rzecz osób fizycznych nieprowadzących działalności gospodarczej oraz rolników ryczałtowych są obowiązani prowadzić ewidencję sprzedaży przy zastosowaniu kas rejestrujących (kas fiskalnych).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 111 ust. 3a pkt 1–11, VAT art. 111 ust. 2, VAT art. 111 ust. 7a): Na podstawie podanych przepisów nie można ustalić, czy usługi naprawy samochodów świadczone osobom prywatnym powodują obowiązek posiadania kasy fiskalnej, ponieważ nie zawierają one treści art. 111 ust. 1 ani innych regulacji określających ten obowiązek. Jeżeli jednak obowiązek ewidencjonowania już powstał albo rozpocząłeś ewidencję na kasie, musisz m.in. wystawiać i wydawać nabywcy paragon fiskalny z każdej sprzedaży oraz poddawać kasę obowiązkowym przeglądom technicznym (VAT art. 111 ust. 3a pkt 1 i 4). Naruszenie obowiązku z art. 111 ust. 1 może skutkować dodatkowym zobowiązaniem podatkowym określonym w VAT art. 111 ust. 2, ale podane przepisy nie pozwalają ocenić, czy dotyczy to Twojej sytuacji.
**Kontekst:** VAT art. 111 ust. 7a, VAT art. 111 ust. 3a pkt 1–11, VAT art. 111 ust. 4, VAT art. 86a ust. 5, VAT art. 111 ust. 2
**Sędzia 1** (claude-sonnet-5): refusal_missing — System odmówił odpowiedzi na kluczowe pytanie (czy obowiązek kasy fiskalnej powstaje), mimo że kontekst wskazuje, że art. 111 ust. 1 istnieje i jest podstawą obowiązku - choć sama treść ust. 1 nie znalazła się w kontekście, inne fragmenty (ust. 2, 3a, 4) jednoznacznie odwołują się do istnienia tego obowiązku dla sprzedaży na rzecz osób fizycznych, więc system mógł/powinien wskazać ogólną zasadę zamiast całkowicie odmawiać.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-01 (fact, oczekiwane: answer)
**Pytanie:** Do kiedy podatnik PIT musi złożyć roczne zeznanie podatkowe za dany rok podatkowy?
**Wzorzec:** Zeznanie roczne składa się w terminie od 15 lutego do 30 kwietnia roku następującego po roku podatkowym. Zeznania złożone wcześniej uznaje się za złożone 15 lutego.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 45 ust. 1): Podatnik PIT musi złożyć roczne zeznanie podatkowe w terminie od 15 lutego do 30 kwietnia roku następującego po danym roku podatkowym. Zeznanie złożone przed 15 lutego uznaje się za złożone 15 lutego.
**Kontekst:** PIT art. 45 ust. 1, PIT art. 44 ust. 7i pkt 3–4, PIT art. 44 ust. 7i pkt 1–2, PIT art. 30de ust. 7, PIT art. 45 ust. 4
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź w pełni zgodna z wzorcem – podaje prawidłowy termin 15 lutego – 30 kwietnia oraz zasadę uznania wcześniejszego złożenia za złożone 15 lutego, zgodnie z PIT art. 45 ust. 1.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-02 (fact, oczekiwane: answer)
**Pytanie:** Jakie są progi i stawki w skali podatkowej PIT z art. 27 ust. 1 oraz jaka jest kwota zmniejszająca podatek?
**Wzorzec:** Dla podstawy obliczenia podatku do 120 000 zł podatek wynosi 12% minus kwota zmniejszająca podatek 3600 zł. Powyżej 120 000 zł podatek wynosi 10 800 zł plus 32% nadwyżki ponad 120 000 zł.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 27 ust. 1): Podstawa obliczenia podatku do 120 000 zł jest opodatkowana stawką 12%, pomniejszoną o kwotę zmniejszającą podatek w wysokości 3 600 zł. Powyżej 120 000 zł podatek wynosi 10 800 zł oraz 32% nadwyżki ponad 120 000 zł.
**Kontekst:** PIT art. 27, PIT art. 26eb, PIT art. 44 ust. 6b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem i przepisem art. 27 ust. 1 – poprawne progi, stawki (12%/32%) i kwota zmniejszająca podatek 3600 zł.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-03 (fact, oczekiwane: answer)
**Pytanie:** Jaką stawkę podatku liniowego stosuje się do dochodów z pozarolniczej działalności gospodarczej, jeśli podatnik wybrał ten sposób opodatkowania?
**Wzorzec:** Podatek dochodowy liniowy od dochodów z pozarolniczej działalności gospodarczej lub działów specjalnych produkcji rolnej wynosi 19% podstawy obliczenia podatku.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 30c ust. 1): Do dochodów z pozarolniczej działalności gospodarczej opodatkowanych podatkiem liniowym stosuje się stawkę 19% podstawy obliczenia podatku. Dotyczy to podatników, o których mowa w PIT art. 9a ust. 2 lub 7, z zastrzeżeniem wyjątków wskazanych w PIT art. 30c ust. 1.
**Kontekst:** PIT art. 26gb, PIT art. 30ca ust. 1, PIT art. 30c, PIT art. 44 ust. 7f, PIT art. 44 ust. 6b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje stawkę 19% podstawy obliczenia podatku zgodnie z art. 30c ust. 1, trafnie odwołując się do podatników z art. 9a ust. 2 lub 7 oraz zastrzeżeń z tego przepisu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-04 (fact, oczekiwane: answer)
**Pytanie:** Ile wynosi ulga na jedno małoletnie dziecko w rozliczeniu PIT (odliczenie miesięczne) i jaki limit dochodów obowiązuje rodzica pozostającego w związku małżeńskim przez cały rok?
**Wzorzec:** Na jedno małoletnie dziecko przysługuje odliczenie 92,67 zł za każdy miesiąc sprawowania opieki, pod warunkiem że dochody podatnika pozostającego przez cały rok w związku małżeńskim i jego małżonka nie przekroczyły w roku podatkowym 112 000 zł.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 27f ust. 1, PIT art. 27f ust. 2 pkt 1 lit. a): Ulga na jedno małoletnie dziecko wynosi 92,67 zł za każdy miesiąc kalendarzowy, w którym podatnik wykonywał władzę rodzicielską, pełnił funkcję opiekuna prawnego albo sprawował opiekę jako rodzina zastępcza. W przypadku podatnika pozostającego przez cały rok podatkowy w związku małżeńskim jego dochody oraz dochody małżonka nie mogą przekroczyć 112 000 zł.
**Kontekst:** PIT art. 27f ust. 2, PIT art. 27f ust. 4, PIT art. 27f ust. 10, PIT art. 27f ust. 1, PIT art. 27f ust. 2c
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje kwotę 92,67 zł miesięcznie oraz limit 112 000 zł dla małżonków, zgodnie z art. 27f ust. 2 pkt 1 lit. a, treść w pełni zgodna z wzorcem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-05 (fact, oczekiwane: answer)
**Pytanie:** Ile wynoszą miesięczne i roczne zryczałtowane koszty uzyskania przychodów ze stosunku pracy dla podatnika zatrudnionego na podstawie jednej umowy o pracę, mieszkającego w miejscowości siedziby zakładu pracy?
**Wzorzec:** Koszty uzyskania przychodów wynoszą 250 zł miesięcznie, a za rok podatkowy łącznie nie więcej niż 3000 zł, jeśli podatnik uzyskuje przychody z tytułu jednego stosunku pracy.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 22 ust. 2 pkt 1): Zryczałtowane koszty uzyskania przychodów wynoszą 250 zł miesięcznie, a za rok podatkowy łącznie nie więcej niż 3000 zł, ponieważ podatnik uzyskuje przychody z jednego stosunku pracy i mieszka w miejscowości, w której znajduje się zakład pracy.
**Kontekst:** PIT art. 22 ust. 2, PIT art. 22 ust. 3b, PIT art. 26he, PIT art. 30 ust. 1 pkt 2–7a, PIT art. 26eb
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje 250 zł/mies. i 3000 zł/rok dla jednego stosunku pracy, zgodnie z art. 22 ust. 2 pkt 1 PIT; wzmianka o zamieszkaniu w miejscowości zakładu pracy jest zgodna z kontekstem (pkt 3 wymaga zamieszkania poza nią, by zastosować wyższą stawkę).
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-06 (fact, oczekiwane: answer)
**Pytanie:** Po jakim okresie posiadania nieruchomości jej sprzedaż nie generuje przychodu podlegającego PIT, zgodnie z art. 10 ust. 1 pkt 8?
**Wzorzec:** Odpłatne zbycie nieruchomości jest zwolnione z opodatkowania, jeśli nastąpiło po upływie pięciu lat, licząc od końca roku kalendarzowego, w którym nastąpiło jej nabycie lub wybudowanie.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 10 ust. 1 pkt 8, PIT art. 10 ust. 5, PIT art. 10 ust. 6): Sprzedaż nieruchomości nie stanowi źródła przychodu z art. 10 ust. 1 pkt 8, jeżeli następuje po upływie pięciu lat, licząc od końca roku kalendarzowego, w którym nastąpiło jej nabycie lub wybudowanie, pod warunkiem że sprzedaż nie następuje w wykonaniu działalności gospodarczej. W przypadku nieruchomości nabytej w spadku okres liczy się od końca roku, w którym nieruchomość nabył lub wybudował spadkodawca; przy majątku wspólnym małżonków — od końca roku nabycia do majątku wspólnego lub wybudowania.
**Kontekst:** PIT art. 10, PIT art. 24 ust. 6
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź w pełni zgodna z wzorcem (5-letni okres liczony od końca roku nabycia/wybudowania) oraz poprawnie i wiernie dodaje istotne uzupełnienia z art. 10 ust. 5 i 6 kontekstu dotyczące spadku i majątku wspólnego małżonków, co wzbogaca odpowiedź bez zmiany sensu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-07 (fact, oczekiwane: answer)
**Pytanie:** Jaką stawkę podatku dochodowego stosuje się do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia?
**Wzorzec:** Podatek dochodowy od dochodu z odpłatnego zbycia nieruchomości i praw określonych w art. 10 ust. 1 pkt 8 lit. a–c wynosi 19% podstawy obliczenia podatku.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 30e ust. 1, PIT art. 30e ust. 2, PIT art. 30e ust. 5): Do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia, stosuje się podatek dochodowy w wysokości 19% podstawy obliczenia podatku. Podstawą jest dochód stanowiący różnicę między przychodem z odpłatnego zbycia a kosztami określonymi w przepisach, powiększoną o sumę wskazanych odpisów amortyzacyjnych. Dochodu tego nie łączy się z dochodami (przychodami) z innych źródeł.
**Kontekst:** PIT art. 21 ust. 1 pkt 29, PIT art. 30e, PIT art. 21 ust. 1 pkt 131–133, PIT art. 21 ust. 1 pkt 29aa–29ab
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje stawkę 19% podstawy obliczenia podatku zgodnie z art. 30e ust. 1, dodatkowo trafnie i zgodnie z kontekstem wyjaśnia sposób ustalenia podstawy (ust. 2) i zakaz łączenia z innymi dochodami (ust. 5), bez treści spoza przepisów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-08 (fact, oczekiwane: answer)
**Pytanie:** Jaki jest miesięczny limit zwolnienia z PIT dla alimentów zasądzonych wyrokiem sądu na rzecz osoby innej niż dziecko?
**Wzorzec:** Alimenty na rzecz innych osób niż dzieci, otrzymane na podstawie wyroku sądu lub ugody sądowej, są wolne od podatku do wysokości nieprzekraczającej miesięcznie 700 zł.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 21 ust. 1 pkt 127 lit. b): Miesięczny limit zwolnienia z PIT dla alimentów otrzymywanych na rzecz osoby innej niż dziecko wynosi 700 zł, jeżeli alimenty są otrzymywane na podstawie wyroku sądu lub ugody sądowej. Wynika to z PIT art. 21 ust. 1 pkt 127 lit. b.
**Kontekst:** PIT art. 21 ust. 1 pkt 125–129a, PIT art. 27f ust. 4, PIT art. 21 ust. 1 pkt 153, PIT art. 27f ust. 1, PIT art. 27f ust. 2e
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź w pełni zgodna z wzorcem i poprawnie cytuje właściwy przepis (art. 21 ust. 1 pkt 127 lit. b).
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-09 (multi, oczekiwane: answer)
**Pytanie:** Kiedy sprzedaż nieruchomości nabytej w drodze spadku jest zwolniona z PIT ze względu na upływ pięciu lat — od kiedy liczy się ten termin?
**Wzorzec:** Zbycie nieruchomości jest zwolnione, jeśli nastąpiło po pięciu latach liczonych od końca roku kalendarzowego nabycia lub wybudowania (art. 10 ust. 1 pkt 8). W przypadku nieruchomości nabytej w drodze spadku termin ten liczy się od końca roku kalendarzowego, w którym nieruchomość nabył lub wybudował spadkodawca, a nie spadkobierca.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 10 ust. 1 pkt 8, PIT art. 10 ust. 5): W przypadku sprzedaży nieruchomości nabytej w drodze spadku pięcioletni termin liczy się od końca roku kalendarzowego, w którym nieruchomość została nabyta lub wybudowana przez spadkodawcę, a nie przez spadkobiercę (PIT art. 10 ust. 5). Po upływie tego terminu odpłatne zbycie nieruchomości, jeżeli nie następuje w wykonaniu działalności gospodarczej, nie mieści się w źródle przychodów określonym w PIT art. 10 ust. 1 pkt 8 lit. a–c.
**Kontekst:** PIT art. 10, PIT art. 21 ust. 1 pkt 29, PIT art. 21 ust. 1 pkt 29aa–29ab
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje, że termin liczy się od nabycia przez spadkodawcę, cytując trafny przepis (art. 10 ust. 5) oraz zasadę pięcioletniego okresu z art. 10 ust. 1 pkt 8, zgodnie z wzorcem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-10 (multi, oczekiwane: answer)
**Pytanie:** Czy podatnik opodatkowany podatkiem liniowym (art. 30c) może rozliczyć się wspólnie z małżonkiem na zasadach art. 6?
**Wzorzec:** Nie. Wspólne opodatkowanie małżonków (art. 6 ust. 2) nie ma zastosowania, jeśli chociażby jeden z małżonków stosuje opodatkowanie podatkiem liniowym na podstawie art. 30c, w zakresie osiągniętych w roku podatkowym przychodów objętych tym sposobem opodatkowania.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 6 ust. 8 pkt 1 lit. a, PIT art. 6 ust. 2): Nie. Wspólne opodatkowanie na zasadach art. 6 ust. 2 nie ma zastosowania, jeżeli chociażby jeden z małżonków stosuje art. 30c w zakresie wskazanym w tym przepisie (PIT art. 6 ust. 8 pkt 1 lit. a).
**Kontekst:** PIT art. 6 ust. 2, PIT art. 6 ust. 3, PIT art. 6a, PIT art. 6 ust. 8, Ordynacja art. 92
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje zakaz wspólnego opodatkowania przy stosowaniu art. 30c, zgodnie z art. 6 ust. 8 pkt 1 lit. a, z właściwym zastrzeżeniem 'w zakresie wskazanym w tym przepisie'.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-11 (multi, oczekiwane: answer)
**Pytanie:** Podatnik rozliczający się podatkiem liniowym (art. 30c) chce pomniejszyć dochód o zapłacone składki zdrowotne — jaki jest roczny limit tego odliczenia i gdzie określono obowiązek zapłaty podatku liniowego w wysokości 19%?
**Wzorzec:** Dochód opodatkowany podatkiem liniowym (19% zgodnie z art. 30c ust. 1) podatnik może pomniejszyć o zapłacone w roku podatkowym składki na ubezpieczenie zdrowotne, przy czym łączna wysokość tych składek zaliczonych do kosztów lub odliczonych od dochodu nie może przekroczyć w roku podatkowym 8700 zł.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 30c ust. 1, PIT art. 30c ust. 2 pkt 2, PIT art. 23 ust. 1 pkt 58): Roczny limit odliczenia zapłaconych składek na ubezpieczenie zdrowotne wynosi 8700 zł; limit obejmuje łącznie składki zaliczone do kosztów uzyskania przychodów lub odliczone od dochodu (PIT art. 30c ust. 2 pkt 2). Obowiązek zapłaty podatku liniowego w wysokości 19% podstawy obliczenia podatku określono w PIT art. 30c ust. 1.
**Kontekst:** PIT art. 30c, PIT art. 44 ust. 6j, PIT art. 27f ust. 9, PIT art. 23 ust. 1 pkt 58–66, PIT art. 26eb
**Sędzia 1** (claude-sonnet-5): correct — Poprawnie podano limit 8700 zł i podstawę prawną 19% (art. 30c ust. 1); treść zgodna z przepisami w kontekście, bez dodatkowych faktów spoza nich.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-12 (multi, oczekiwane: answer)
**Pytanie:** Rodzic samotnie wychowujący dwójkę małoletnich dzieci chce skorzystać z preferencyjnego rozliczenia podatku jako osoba samotnie wychowująca dzieci oraz z ulgi na dzieci — ile wynosi ulga na dwoje małoletnich dzieci i na jakich warunkach przysługuje preferencyjne rozliczenie samotnego rodzica?
**Wzorzec:** Na dwoje małoletnich dzieci odliczeniu podlega 92,67 zł na każde dziecko za każdy miesiąc sprawowania opieki; dla dwojga dzieci ustawa nie przewiduje limitu dochodu. Rodzic samotnie wychowujący małoletnie dzieci (m.in. panna, kawaler, wdowa, wdowiec, rozwódka, rozwodnik) może na wniosek w zeznaniu rocznym określić podatek w podwójnej wysokości podatku obliczonego od połowy swoich dochodów.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 27f ust. 2, PIT art. 27f ust. 1, PIT art. 27f ust. 4, PIT art. 6 ust. 4c, PIT art. 6 ust. 4f): Ulga na dwoje małoletnich dzieci wynosi 92,67 zł na każde dziecko za każdy miesiąc roku podatkowego, w którym podatnik wykonywał władzę rodzicielską, pełnił funkcję opiekuna prawnego przy wspólnym zamieszkiwaniu z dzieckiem albo sprawował opiekę jako rodzina zastępcza; łącznie jest to 185,34 zł za taki miesiąc. Odliczenie przysługuje łącznie obojgu rodzicom lub opiekunom i może być podzielone w dowolnej proporcji, a przy braku porozumienia — w przypadkach wskazanych w przepisie — w częściach równych albo w wysokości 100% podatnikowi, u którego dziecko ma miejsce zamieszkania. Preferencyjne rozliczenie może dotyczyć jednego rodzica podlegającego obowiązkowi podatkowemu, który jest m.in. panną, kawalerem, wdową, wdowcem, rozwódką, rozwodnikiem albo osobą w separacji i który w roku podatkowym samotnie wychowuje dzieci; wymaga ono wniosku wyrażonego w rocznym zeznaniu podatkowym. Z przedstawionych przepisów wynika również, że preferencja nie ma zastosowania, gdy rodzic wychowuje wspólnie z drugim rodzicem albo opiekunem prawnym co najmniej jedno dziecko, w tym przy opiece naprzemiennej, jeżeli obojgu rodzicom ustalono świadczenie wychowawcze; przepisy nie określają jednak w podanym materiale sposobu obliczenia podatku według tej preferencji.
**Kontekst:** PIT art. 27f ust. 2, PIT art. 6 ust. 4f, PIT art. 27f ust. 4, PIT art. 6 ust. 4c, PIT art. 27f ust. 1
**Sędzia 1** (claude-sonnet-5): partial — Kwota ulgi (92,67 zł/dziecko) i warunki samotnego rodzica podane prawidłowo, ale system nie podał kluczowej informacji ze wzorca, że samotny rodzic może określić podatek w podwójnej wysokości podatku obliczonego od połowy dochodów - wprost przyznał, że nie znalazł w materiale sposobu obliczenia podatku według tej preferencji, mimo że ta informacja powinna być dostępna (art. 6 ust. 4d), co jest istotnym pominięciem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-13 (colloquial, oczekiwane: answer)
**Pytanie:** Sprzedałem mieszkanie i całą kwotę zamierzam w ciągu najbliższych 2 lat wydać na zakup innego mieszkania na własne potrzeby — czy muszę zapłacić podatek od tej sprzedaży?
**Wzorzec:** Dochód ze sprzedaży jest zwolniony z podatku w części odpowiadającej udziałowi wydatków na własne cele mieszkaniowe w przychodzie ze zbycia, pod warunkiem że przychód zostanie wydatkowany na te cele nie później niż w okresie trzech lat od końca roku podatkowego, w którym nastąpiło zbycie. Wydatkowanie całej kwoty w ciągu 2 lat mieści się w tym trzyletnim terminie, więc przy spełnieniu warunków dochód będzie zwolniony z PIT.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 21 ust. 1 pkt 131): Nie można rozstrzygnąć tego bez daty sprzedaży i potwierdzenia, że zakup będzie własnym celem mieszkaniowym. Dochód ze sprzedaży może być zwolniony w części odpowiadającej udziałowi udokumentowanych wydatków na własne cele mieszkaniowe w przychodzie ze sprzedaży, jeżeli przychód zostanie wydatkowany od dnia sprzedaży, nie później niż w ciągu trzech lat od końca roku podatkowego, w którym nastąpiła sprzedaż; wydatki uwzględnia się do wysokości tego przychodu (PIT art. 21 ust. 1 pkt 131). Jeżeli cała kwota przychodu zostanie w tym terminie wydana na zakup mieszkania na własne potrzeby i spełnione są pozostałe warunki przepisu, wynikająca z niego ulga obejmuje cały dochód objęty tym przepisem; potrzebne jest także udokumentowanie wydatków.
**Kontekst:** PIT art. 21 ust. 1 pkt 29, PIT art. 21 ust. 1 pkt 131–133, VAT art. 111 ust. 6, Ordynacja art. 59
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie przytacza art. 21 ust. 1 pkt 131 PIT, wyjaśnia zasadę proporcjonalnego zwolnienia i 3-letni termin, zgodnie z wzorcem; dodatkowe zastrzeżenia (potwierdzenie daty, dokumentacja wydatków) nie są błędem, lecz uzupełnieniem wynikającym z przepisu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-14 (colloquial, oczekiwane: answer)
**Pytanie:** Pracuję na jednym etacie w tej samej miejscowości, w której mieszkam — o ile mogę pomniejszyć swój przychód z tytułu kosztów uzyskania przychodu w ciągu roku?
**Wzorzec:** Przy jednym stosunku pracy w miejscowości zamieszkania koszty uzyskania przychodów wynoszą 250 zł miesięcznie, czyli maksymalnie 3000 zł za cały rok podatkowy.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 22 ust. 2 pkt 1): Przy jednym stosunku pracy możesz pomniejszyć przychód o koszty uzyskania przychodów w wysokości 250 zł miesięcznie, łącznie nie więcej niż 3000 zł za rok podatkowy. Dotyczy to sytuacji, gdy miejsce zamieszkania znajduje się w tej samej miejscowości co zakład pracy.
**Kontekst:** PIT art. 22 ust. 2, PIT art. 22 ust. 9 pkt 5–6, PIT art. 22 ust. 11, PIT art. 22 ust. 7b, PIT art. 22 ust. 9a
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje kwotę 250 zł miesięcznie / 3000 zł rocznie zgodnie z art. 22 ust. 2 pkt 1, zgodnie z wzorcem i opisanymi warunkami (jeden stosunek pracy, miejscowość zamieszkania = zakład pracy).
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-15 (colloquial, oczekiwane: answer)
**Pytanie:** Płacę byłej żonie alimenty na jej rzecz (nie na dziecko) zasądzone wyrokiem sądu w wysokości 900 zł miesięcznie — czy ona musi zapłacić podatek od tej kwoty?
**Wzorzec:** Alimenty na rzecz osoby innej niż dziecko, zasądzone wyrokiem sądu, są wolne od podatku tylko do wysokości 700 zł miesięcznie. Nadwyżka ponad tę kwotę, czyli 200 zł miesięcznie, podlega opodatkowaniu.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 21 ust. 1 pkt 127 lit. b): Na podstawie podanego przepisu alimenty na rzecz byłej żony, otrzymane na podstawie wyroku sądu, są zwolnione z podatku do wysokości 700 zł miesięcznie (PIT art. 21 ust. 1 pkt 127 lit. b). Z kwoty 900 zł miesięcznie zwolnieniem objęte jest więc 700 zł, natomiast 200 zł nie jest objęte tym zwolnieniem. W przekazanych przepisach nie ma informacji pozwalających ustalić, czy od tej pozostałej kwoty była żona faktycznie musi zapłacić podatek ani w jakiej wysokości.
**Kontekst:** PIT art. 27f ust. 4, PIT art. 27f ust. 2, Ordynacja art. 119zy, PIT art. 41 ust. 12, PIT art. 21 ust. 1 pkt 125–129a
**Sędzia 1** (claude-sonnet-5): partial — System prawidłowo zidentyfikował limit 700 zł i nadwyżkę 200 zł, ale nie dopowiedział wprost (jak wzorzec), że ta nadwyżka podlega opodatkowaniu - zamiast tego odmówił stwierdzenia tego faktu, mimo że wynika on logicznie z przepisu (zwolnienie tylko do 700 zł oznacza, że reszta jest opodatkowana).
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-01 (fact, oczekiwane: answer)
**Pytanie:** Po jakim okresie przedawnia się zobowiązanie podatkowe, licząc od terminu płatności podatku?
**Wzorzec:** Zobowiązanie podatkowe przedawnia się z upływem 5 lat, licząc od końca roku kalendarzowego, w którym upłynął termin płatności podatku.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 70 § 1, Ordynacja art. 70 § 1a pkt 1–2, Ordynacja art. 70 § 1a pkt 3, Ordynacja art. 70 § 1b): Zobowiązanie podatkowe przedawnia się po upływie 5 lat, licząc od końca roku kalendarzowego, w którym upłynął termin płatności podatku. Dla niektórych zobowiązań podatników podatku dochodowego od osób prawnych przepisy przewidują odrębny sposób ustalania początku tego okresu.
**Kontekst:** Ordynacja art. 70 § 1, Ordynacja art. 70 § 1b, Ordynacja art. 70 § 1a pkt 3, Ordynacja art. 70 § 1a pkt 1–2, Ordynacja art. 80
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje główną zasadę (5 lat od końca roku kalendarzowego, w którym upłynął termin płatności) i trafnie sygnalizuje istnienie wyjątków dla CIT bez wprowadzania błędnych szczegółów, co w pełni opiera się na przytoczonych przepisach.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-02 (fact, oczekiwane: answer)
**Pytanie:** Jaka jest wysokość stawki odsetek za zwłokę od zaległości podatkowych?
**Wzorzec:** Stawka odsetek za zwłokę jest równa sumie 200% podstawowej stopy oprocentowania kredytu lombardowego i 2%, z tym że nie może być niższa niż 8%.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 56 § 1, Ordynacja art. 56a § 1, Ordynacja art. 56b): Podstawowa stawka odsetek za zwłokę wynosi 200% podstawowej stopy oprocentowania kredytu lombardowego ustalanej zgodnie z przepisami o NBP, powiększone o 2%, przy czym nie może być niższa niż 8% (Ordynacja art. 56 § 1). W określonych przypadkach stosuje się stawkę obniżoną w wysokości 50% stawki podstawowej (Ordynacja art. 56a § 1) albo stawkę podwyższoną w wysokości 150% stawki podstawowej, dotyczącą zaległości w VAT i podatku akcyzowym po spełnieniu warunków z Ordynacja art. 56b.
**Kontekst:** Ordynacja art. 56, Ordynacja art. 56a, Ordynacja art. 57, Ordynacja art. 55, Ordynacja art. 56b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem (200% stopy lombardowej + 2%, min. 8%), a dodatkowe informacje o stawce obniżonej i podwyższonej są prawidłowo oparte na przepisach z kontekstu i nie zmieniają sensu odpowiedzi na zadane pytanie.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-03 (fact, oczekiwane: answer)
**Pytanie:** Co uznaje się za nadpłatę podatku zgodnie z Ordynacją podatkową?
**Wzorzec:** Za nadpłatę uważa się m.in. kwotę nadpłaconego lub nienależnie zapłaconego podatku oraz kwotę podatku pobraną przez płatnika nienależnie lub w wysokości większej od należnej.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 72 § 1, Ordynacja art. 72 § 1a–1b, Ordynacja art. 72 § 2): Za nadpłatę uważa się kwotę nadpłaconego lub nienależnie zapłaconego podatku, a także podatek pobrany przez płatnika nienależnie albo w wysokości większej od należnej (Ordynacja art. 72 § 1 pkt 1–2). Nadpłatą jest również określone w przepisie zobowiązanie zapłacone przez płatnika, inkasenta, osobę trzecią lub spadkobiercę, jeżeli określono je nienależnie albo w wysokości większej od należnej (Ordynacja art. 72 § 1 pkt 3–4). Na równi z nadpłatą traktuje się także określone różnice wykazane w zeznaniu PIT, kwoty przysługujące podatnikowi na podstawie wskazanych przepisów oraz część wpłaty zaliczoną na odsetki za zwłokę i nienależnie zapłacone zaległości, odsetki lub opłatę prolongacyjną (Ordynacja art. 72 § 1a–1b i § 2).
**Kontekst:** Ordynacja art. 77c, Ordynacja art. 72, Ordynacja art. 75, Ordynacja art. 78a
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź dokładnie odwzorowuje treść art. 72 § 1-2 oraz § 1a-1b, trafnie cytuje przepisy i nie zawiera błędów ani informacji spoza kontekstu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-04 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie organ podatkowy powinien wydać interpretację indywidualną przepisów prawa podatkowego od dnia otrzymania wniosku?
**Wzorzec:** Interpretację indywidualną wydaje się bez zbędnej zwłoki, jednak nie później niż w terminie 3 miesięcy od dnia otrzymania wniosku.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 14d § 1): Organ podatkowy powinien wydać interpretację indywidualną bez zbędnej zwłoki, nie później niż w terminie 3 miesięcy od dnia otrzymania wniosku. Do tego terminu nie wlicza się terminów i okresów, o których mowa w Ordynacja art. 139 § 4.
**Kontekst:** Ordynacja art. 14d, Ordynacja art. 14o, Ordynacja art. 14m
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem (3 miesiące, bez zbędnej zwłoki), dodatkowa informacja o niewliczaniu terminów z art. 139 § 4 jest poprawna i wynika z cytowanego przepisu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-05 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie od dnia doręczenia decyzji wnosi się odwołanie?
**Wzorzec:** Odwołanie wnosi się w terminie 14 dni od dnia doręczenia decyzji stronie.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 223 § 1, Ordynacja art. 223 § 2 pkt 1): Odwołanie wnosi się w terminie 14 dni od dnia doręczenia decyzji stronie, do właściwego organu odwoławczego za pośrednictwem organu podatkowego, który wydał decyzję.
**Kontekst:** Ordynacja art. 223, Ordynacja art. 213, Ordynacja art. 227, Ordynacja art. 236
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem i poprawnie uzupełniona o informację z art. 223 § 1 dotyczącą trybu wniesienia odwołania, co nie zmienia sensu i jest poparte przepisami w kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-06 (fact, oczekiwane: answer)
**Pytanie:** Czy podatnik ma prawo skorygować uprzednio złożoną deklarację podatkową?
**Wzorzec:** Tak, jeżeli odrębne przepisy nie stanowią inaczej, podatnicy, płatnicy i inkasenci mogą skorygować uprzednio złożoną deklarację.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 81 § 1–2, Ordynacja art. 81b § 1 pkt 1 i § 2): Tak. Jeżeli odrębne przepisy nie stanowią inaczej, podatnik może skorygować uprzednio złożoną deklarację przez złożenie deklaracji korygującej (Ordynacja art. 81 § 1–2). Uprawnienie to jest zawieszone na czas trwania postępowania podatkowego lub kontroli podatkowej w zakresie nimi objętym, a korekta złożona w tym czasie nie wywołuje skutków prawnych (Ordynacja art. 81b § 1 pkt 1 i § 2).
**Kontekst:** Ordynacja art. 81, Ordynacja art. 81b, Ordynacja art. 75
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź potwierdza prawo do korekty zgodnie z art. 81 i dodatkowo trafnie wskazuje zawieszenie tego uprawnienia z art. 81b, co jest istotnym uzupełnieniem, nie sprzecznym z wzorcem. Drobna nieścisłość (pominięcie płatników/inkasentów w pierwszym zdaniu) nie zmienia sensu odpowiedzi.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-07 (multi, oczekiwane: answer)
**Pytanie:** Czy podatnik może skorygować deklarację w trakcie trwającego postępowania podatkowego i czy po jego zakończeniu prawo to wraca?
**Wzorzec:** Uprawnienie do skorygowania deklaracji ulega zawieszeniu na czas trwania postępowania podatkowego lub kontroli podatkowej w zakresie nią objętym — co do zasady podatnik może skorygować uprzednio złożoną deklarację (art. 81 § 1), ale to prawo przysługuje nadal dopiero po zakończeniu kontroli podatkowej albo postępowania podatkowego w zakresie nieobjętym decyzją określającą wysokość zobowiązania.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 81b § 1 pkt 1–2, Ordynacja art. 81b § 2, Ordynacja art. 81b § 1a): W trakcie postępowania podatkowego prawo do skorygowania deklaracji ulega zawieszeniu w zakresie objętym tym postępowaniem, a korekta złożona w tym czasie nie wywołuje skutków prawnych. Po zakończeniu postępowania prawo do korekty przysługuje nadal w zakresie nieobjętym decyzją określającą wysokość zobowiązania podatkowego. Wyjątkiem jest postępowanie dotyczące unikania opodatkowania, w którym podatnik może jednokrotnie skorygować deklarację przed wydaniem decyzji w pierwszej instancji, w terminie i na zasadach określonych w Ordynacja art. 81b § 1a.
**Kontekst:** Ordynacja art. 81b, Ordynacja art. 81, Ordynacja art. 274, Ordynacja art. 75
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie opisuje zawieszenie prawa do korekty w zakresie objętym postępowaniem, bezskuteczność korekty w tym czasie, powrót prawa po zakończeniu w zakresie nieobjętym decyzją, oraz trafnie dodaje wyjątek z art. 81b §1a dotyczący unikania opodatkowania - wszystko zgodne z przepisami w kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-09 (multi, oczekiwane: answer)
**Pytanie:** Czy wniesienie skargi do sądu administracyjnego na decyzję podatkową wpływa na bieg 5-letniego terminu przedawnienia zobowiązania podatkowego?
**Wzorzec:** Tak. Zobowiązanie podatkowe przedawnia się co do zasady z upływem 5 lat od końca roku, w którym upłynął termin płatności podatku, ale bieg tego terminu nie rozpoczyna się, a rozpoczęty ulega zawieszeniu z dniem wniesienia skargi do sądu administracyjnego na decyzję dotyczącą tego zobowiązania.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 70 § 6 pkt 2, Ordynacja art. 70 § 7 pkt 2): Tak. Wniesienie skargi do sądu administracyjnego na decyzję dotyczącą tego zobowiązania powoduje, że bieg terminu przedawnienia — także 5-letniego, jeżeli ma zastosowanie — nie rozpoczyna się albo rozpoczęty ulega zawieszeniu od dnia wniesienia skargi (Ordynacja art. 70 § 6 pkt 2). Po zawieszeniu termin biegnie dalej od dnia następującego po dniu doręczenia organowi podatkowemu odpisu prawomocnego orzeczenia sądu administracyjnego (Ordynacja art. 70 § 7 pkt 2).
**Kontekst:** Ordynacja art. 70e, Ordynacja art. 68, Ordynacja art. 70 § 6 pkt 1–6, Ordynacja art. 70 § 7, Ordynacja art. 70c
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje mechanizm zawieszenia/nierozpoczęcia biegu terminu z art. 70 §6 pkt 2 i jego dalszy bieg po art. 70 §7 pkt 2, co odpowiada wzorcowi; cytaty zgodne z podanym kontekstem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-10 (colloquial, oczekiwane: answer)
**Pytanie:** Dostałem decyzję z urzędu skarbowego, z którą się nie zgadzam — ile czasu mam na złożenie odwołania i do kogo je składam?
**Wzorzec:** Odwołanie wnosi się w terminie 14 dni od dnia doręczenia decyzji, składając je do właściwego organu odwoławczego za pośrednictwem organu podatkowego, który wydał decyzję.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 223 § 1–2, Ordynacja art. 221 § 1–2): Odwołanie należy wnieść w terminie 14 dni od dnia doręczenia decyzji. Składa się je do właściwego organu odwoławczego za pośrednictwem organu podatkowego, który wydał decyzję, czyli urzędu skarbowego. Jeżeli decyzję w pierwszej instancji wydał organ wymieniony w Ordynacja art. 221 § 1–2, odwołanie rozpatruje ten sam organ.
**Kontekst:** Ordynacja art. 223, Ordynacja art. 227, Ordynacja art. 221, Ordynacja art. 233, Ordynacja art. 226
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje termin 14 dni i tryb wnoszenia odwołania za pośrednictwem organu wydającego decyzję, zgodnie z art. 223; dodatkowa uwaga o art. 221 jest prawdziwa, choć nieistotna dla typowego urzędu skarbowego, i nie wprowadza błędu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-11 (colloquial, oczekiwane: answer)
**Pytanie:** Mój księgowy ma moje pełnomocnictwo do wszystkich moich spraw podatkowych w ogóle, a nie tylko do jednej konkretnej kontroli — jak nazywa się taki rodzaj pełnomocnictwa i co obejmuje?
**Wzorzec:** To jest pełnomocnictwo ogólne. Upoważnia ono pełnomocnika do działania we wszystkich sprawach podatkowych oraz w innych sprawach należących do właściwości organów podatkowych, w odróżnieniu od pełnomocnictwa szczególnego dotyczącego konkretnej sprawy.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 138d § 1, Ordynacja art. 138a § 1, Ordynacja art. 138a § 2): Jest to pełnomocnictwo ogólne. Upoważnia do działania we wszystkich sprawach podatkowych oraz w innych sprawach należących do właściwości organów podatkowych. Nie obejmuje jednak czynności, których charakter wymaga osobistego działania strony. 
**Kontekst:** Ordynacja art. 138d, Ordynacja art. 138e, Ordynacja art. 138a, Ordynacja art. 86na, Ordynacja art. 138g
**Sędzia 1** (claude-sonnet-5): correct — Trafnie identyfikuje pełnomocnictwo ogólne i jego zakres zgodnie z art. 138d §1; dodatkowa uwaga o wyłączeniu czynności wymagających osobistego działania wynika z art. 138a §1 i jest zgodna z kontekstem, nie zmienia sensu odpowiedzi.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-02 (out_of_corpus, oczekiwane: refuse)
**Pytanie:** Napisz mi krótki wiersz o jesieni.
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie — nie dotyczy ono prawa podatkowego, a zajmuję się wyłącznie przepisami podatkowymi.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na prośbę o napisanie wiersza o jesieni.
**Kontekst:** PIT art. 22j ust. 1, Ordynacja art. 20zj, PIT art. 22j ust. 8, PIT art. 5a pkt 36–40, PIT art. 22j ust. 6
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie odmówił odpowiedzi na pytanie niepodatkowe, zgodnie z zakresem przepisów, tak jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił odpowiedzi na pytanie pozapodatkowe, zgodnie z oczekiwanym zachowaniem. Nie dodał żadnych twierdzeń spoza przekazanego kontekstu.

## hyde/verify=off · g-ooc-03 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaka jest stawka podatku CIT dla małych podatników w 2026 roku?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa — stan na 2026-08-26 / 2026-04-01 / 2026-04-21), nie ma odpowiedzi na to pytanie. Stawki podatku dochodowego od osób prawnych (CIT), w tym stawkę dla małych podatników, reguluje ustawa o podatku dochodowym od osób prawnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na pytanie o stawkę podatku CIT dla małych podatników w 2026 roku. Dotyczy to ustawy o podatku dochodowym od osób prawnych (CIT), której przepisów nie udostępniono.
**Kontekst:** VAT art. 99 ust. 3, PIT art. 22k ust. 7, VAT art. 91 ust. 1b, VAT art. 90 ust. 10, PIT art. 44 ust. 6b
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, wskazując, że stawka CIT dla małych podatników jest regulowana w ustawie o CIT, nieobjętej kontekstem; odpowiedź zgodna z wzorcem i nie zawiera twierdzeń spoza przepisów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-04 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Ile wynosi akcyza na litr benzyny bezołowiowej?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki podatku akcyzowego na paliwa reguluje ustawa o podatku akcyzowym, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma informacji o wysokości akcyzy na litr benzyny bezołowiowej. Podane przepisy dotyczą podatku od towarów i usług, a nie podatku akcyzowego.
**Kontekst:** VAT art. 103 ust. 5aa pkt 1–10, VAT art. 77, VAT art. 41 ust. 3–4, VAT art. 52, VAT art. 41 ust. 5
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, wskazując że dostępne przepisy dotyczą VAT, nie akcyzy; nie dopowiedział żadnej liczby/stawki spoza kontekstu, choć nie wskazał konkretnej nazwy ustawy o podatku akcyzowym jak wzorzec.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-05 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaki jest podatek PCC od zakupu mieszkania z rynku wtórnego?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Podatek od czynności cywilnoprawnych (PCC), w tym jego stawkę przy zakupie nieruchomości, reguluje ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej podatku PCC od zakupu mieszkania z rynku wtórnego.
**Kontekst:** VAT art. 7, VAT art. 43 ust. 1 pkt 10a–11, PIT art. 24 ust. 24, VAT art. 111 ust. 2, VAT art. 26
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, bo PCC nie jest w przepisach VAT/PIT/Ordynacja; odpowiedź nie dodaje żadnych faktów spoza kontekstu, choć nie wskazuje wprost właściwej ustawy jak wzorzec.
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo odmówił odpowiedzi, ponieważ przekazane przepisy nie regulują PCC ani jego stawki przy zakupie mieszkania. Nie dodał żadnych informacji spoza kontekstu.

## hyde/verify=off · g-ooc-06 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaką stawkę podatku od spadków i darowizn płaci się przy darowiźnie od rodzica dla dziecka?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki i zwolnienia w podatku od spadków i darowizn, w tym dla najbliższej rodziny, reguluje ustawa o podatku od spadków i darowizn, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma informacji o stawkach podatku od spadków i darowizn ani o opodatkowaniu darowizny od rodzica dla dziecka.
**Kontekst:** PIT art. 22 ust. 6d, PIT art. 26 ust. 6c–6d, Ordynacja art. 105, PIT art. 23 ust. 1 pkt 10–14, PIT art. 27f ust. 4
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił odpowiedzi, ponieważ temat nie jest regulowany przepisami w kontekście; nie wskazał jednak nazwy właściwej ustawy, co jest drobnym niedociągnięciem, ale nie wpływa na poprawność odmowy.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-07 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Ile wynosi w 2026 roku składka zdrowotna dla przedsiębiorcy na podatku liniowym?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Wysokość i zasady składki na ubezpieczenie zdrowotne reguluje ustawa o świadczeniach opieki zdrowotnej finansowanych ze środków publicznych, która nie jest częścią mojego korpusu — PIT pozwala jedynie odliczyć zapłaconą składkę zdrowotną od dochodu, nie określa jej wysokości.
**Odpowiedź** (odmowa=True; cytaty: PIT art. 30c ust. 2 pkt 2, PIT art. 23 ust. 1 pkt 58, PIT art. 44 ust. 6j): W udostępnionych przepisach nie określono wysokości składki zdrowotnej dla przedsiębiorcy opodatkowanego podatkiem liniowym w 2026 roku. Wynika z nich jedynie, że zapłacone składki mogą być uwzględniane przy podatku liniowym, a ich łączna wysokość zaliczona do kosztów lub odliczona od dochodu nie może przekroczyć 8700 zł (PIT art. 30c ust. 2 pkt 2, PIT art. 23 ust. 1 pkt 58); zaliczkę można także obniżyć o 19% zapłaconej składki (PIT art. 44 ust. 6j).
**Kontekst:** PIT art. 23 ust. 1 pkt 58–66, PIT art. 30c, PIT art. 44 ust. 6j, PIT art. 27f ust. 9
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił podania wysokości składki (nie jest w kontekście) i trafnie wskazał powiązane przepisy PIT dotyczące limitu odliczenia/kosztu (8700 zł) oraz obniżki zaliczki o 19% – wszystko zgodne z podanym kontekstem, nic nie dopowiedziano spoza niego.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-08 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jakie są stawki ryczałtu od przychodów ewidencjonowanych dla usług budowlanych?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki ryczałtu od przychodów ewidencjonowanych reguluje ustawa o zryczałtowanym podatku dochodowym od niektórych przychodów osiąganych przez osoby fizyczne, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: PIT art. 24b ust. 2): W przepisach, które mam, nie ma odpowiedzi na pytanie o stawki ryczałtu od przychodów ewidencjonowanych dla usług budowlanych. PIT art. 24b ust. 2 wskazuje jedynie wskaźnik dochodu stosowany przy oszacowaniu dochodu, a nie stawkę ryczałtu od przychodów ewidencjonowanych.
**Kontekst:** PIT art. 22i, PIT art. 24b, VAT art. 41 ust. 12, VAT art. 85, VAT art. 114, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, wskazując brak odpowiedzi w dostępnych przepisach; cytowanie PIT art. 24b (wskaźnik dochodu z oszacowania, nie stawka ryczałtu) jest zgodne z kontekstem i trafnie odróżnia te kwestie.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-10 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Ile kosztuje opłata skarbowa za pełnomocnictwo złożone w urzędzie skarbowym?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Wysokość opłaty skarbowej za pełnomocnictwo reguluje ustawa o opłacie skarbowej, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: Ordynacja art. 80a): W przepisach, które mam, nie ma informacji o wysokości opłaty skarbowej za pełnomocnictwo złożone w urzędzie skarbowym. Ordynacja podatkowa określa jedynie zasady składania pełnomocnictwa do podpisywania deklaracji, ale nie określa opłaty skarbowej za jego złożenie. Odpowiedzi należy szukać w ustawie o opłacie skarbowej.
**Kontekst:** Ordynacja art. 299 § 6a, Ordynacja art. 14za, Ordynacja art. 80a, Ordynacja art. 138h, Ordynacja art. 119zc
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił i wskazał, że odpowiedź jest w ustawie o opłacie skarbowej, zgodnie z wzorcem; dodatkowa informacja o art. 80a jest trafnym kontekstem i wynika z przepisów w kontekście.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-11 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaka kara grozi za niewystawienie faktury zgodnie z Kodeksem karnym skarbowym?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Odpowiedzialność karną skarbową, w tym kary za niewystawienie faktury, reguluje Kodeks karny skarbowy, który nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 106ni): W przekazanych przepisach nie ma odpowiedzi, jaka kara grozi za niewystawienie faktury na podstawie Kodeksu karnego skarbowego. VAT art. 106ni przewiduje natomiast karę pieniężną za określone naruszenia dotyczące faktury ustrukturyzowanej, ale nie określa kary z Kodeksu karnego skarbowego.
**Kontekst:** VAT art. 106ni, VAT art. 106e ust. 12, VAT art. 106b
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił odpowiedzi na pytanie o Kodeks karny skarbowy, jednocześnie wskazując dodatkowo trafną informację z VAT art. 106ni o karze pieniężnej za inne naruszenia - to jest zgodne z kontekstem i nie zawiera dopowiedzeń spoza przepisów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-12 (out_of_corpus, oczekiwane: answer_with_date)
**Pytanie:** Jaki limit zwolnienia podmiotowego z VAT będzie obowiązywał w 2028 roku?
**Wzorzec:** Mam dostęp do ustawy o VAT w stanie prawnym na 2026-08-26. Obecnie (stan na tę datę) limit zwolnienia podmiotowego z VAT wynosi 240 000 zł (art. 113 ust. 1 ustawy o VAT). Korpus nie zawiera żadnego przepisu przejściowego ani zapowiedzi zmiany tego limitu na 2028 rok, więc nie mogę potwierdzić, czy i jak zmieni się on w przyszłości.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 113a ust. 1 pkt 2): W przepisach, które mam, nie ma informacji określającej limit zwolnienia podmiotowego z VAT obowiązujący w 2028 roku. VAT art. 113a ust. 1 pkt 2 odwołuje się do limitu z VAT art. 113 ust. 1, którego treści nie podano.
**Kontekst:** VAT art. 52, VAT art. 43 ust. 24, VAT art. 43 ust. 23, VAT art. 49, VAT art. 113a
**Sędzia 1** (claude-sonnet-5): refusal_ok — System trafnie odmówił podania limitu na 2028 rok, bo w podanym kontekście brakuje treści art. 113 ust. 1 (nie podano konkretnej kwoty), co jest zgodne z oczekiwaną odmową; choć nie podał daty stanu prawnego ani kwoty 240 000 zł obowiązującej obecnie, nie dodał żadnych informacji spoza kontekstu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-13 (out_of_corpus, oczekiwane: refuse)
**Pytanie:** Ile wynosiła kwota wolna od podatku PIT w 2015 roku?
**Wzorzec:** W przepisach, które mam (PIT, stan na 2026-04-01), nie ma odpowiedzi na to pytanie. Korpus zawiera aktualny stan prawny ustawy o PIT, a nie jej historyczne wersje — nie mogę podać wysokości kwoty wolnej/kwoty zmniejszającej podatek obowiązującej w 2015 roku.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma informacji o kwocie wolnej od podatku PIT w 2015 roku; podane przepisy dotyczą stanu prawnego na 2026-04-01.
**Kontekst:** PIT art. 27, PIT art. 21 ust. 1 pkt 151–152, PIT art. 30e, PIT art. 21 ust. 1 pkt 153, PIT art. 21 ust. 1 pkt 25c–26b
**Sędzia 1** (claude-sonnet-5): correct — System poprawnie odmówił podania historycznej kwoty wolnej z 2015 r., wskazując, że kontekst zawiera tylko aktualny stan prawny (2026-04-01), co jest zgodne z wzorcem i nie dodaje żadnych informacji spoza przepisów.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-14 (out_of_corpus, oczekiwane: refuse)
**Pytanie:** Jaka stawka VAT na żywność obowiązywała w Polsce w 2010 roku?
**Wzorzec:** W przepisach, które mam (ustawa o VAT, stan na 2026-08-26), nie ma stawek obowiązujących w 2010 roku — korpus zawiera tekst obecny, a przepisy przejściowe dotyczą innych okresów. Nie mogę podać historycznej stawki.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej stawki VAT na żywność obowiązującej w 2010 roku, ponieważ podane przepisy mają stan prawny z 2026 roku. Właściwą ustawą jest ustawa o VAT, ale do ustalenia stawki w 2010 roku potrzebne są przepisy obowiązujące w tym okresie.
**Kontekst:** VAT art. 41 ust. 12f, VAT art. 41 ust. 2, VAT art. 41 ust. 2a, VAT art. 85, VAT art. 146eg, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił podania historycznej stawki VAT z 2010 roku, trafnie wskazując, że dostępne przepisy mają aktualny stan prawny, co jest zgodne z wzorcem.
**Sędzia 2** (): error — 

## hyde/verify=off · g-pit-16 (multi, oczekiwane: answer)
**Pytanie:** Prowadzę jednoosobową działalność i kupiłem laptopa do pracy za 6000 zł. Czy mogę cały wydatek wrzucić w koszty od razu, czy muszę go amortyzować?
**Wzorzec:** Można zaliczyć wydatek od razu: podatnicy mogą nie dokonywać odpisów amortyzacyjnych od składników majątku o wartości początkowej nieprzekraczającej 10 000 zł — wydatki na ich nabycie stanowią wtedy koszty uzyskania przychodów w miesiącu oddania do używania (PIT art. 22d ust. 1). Laptop za 6000 zł mieści się w tym limicie.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 22g ust. 1 pkt 1, PIT art. 22d ust. 1, PIT art. 22f ust. 3): Jeżeli wartość początkowa laptopa, ustalona jako cena nabycia, wynosi 6000 zł, możesz nie dokonywać odpisów amortyzacyjnych, a wydatek zaliczyć jednorazowo do kosztów uzyskania przychodów w miesiącu oddania laptopa do używania (PIT art. 22g ust. 1 pkt 1; PIT art. 22d ust. 1). Nie musisz go amortyzować, ponieważ jego wartość początkowa nie przekracza 10 000 zł; przepisy pozwalają także na amortyzację albo jednorazowy odpis w miesiącu oddania do używania lub w miesiącu następnym (PIT art. 22f ust. 3).
**Kontekst:** PIT art. 22k ust. 14, PIT art. 22d, PIT art. 22g ust. 1 pkt 1–4, PIT art. 22f, PIT art. 22e
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje, że przy wartości 6000 zł można nie amortyzować i zaliczyć wydatek jednorazowo w koszty (art. 22d ust. 1), zgodnie z wzorcem; dodatkowe odniesienie do art. 22f ust. 3 i 22g ust. 1 pkt 1 jest trafne i wynika z podanych przepisów, bez treści spoza kontekstu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-16 (out_of_corpus, oczekiwane: provisions_without_verdict)
**Pytanie:** Sprzedałem mieszkanie, które odziedziczyłem po rodzicach 4 lata temu. Czy zapłacę podatek PIT od tej sprzedaży w moim przypadku?
**Wzorzec:** Mogę przytoczyć przepisy, które regulują tę kwestię: PIT art. 10 ust. 1 pkt 8 lit. a wiąże obowiązek podatkowy ze zbyciem nieruchomości przed upływem pięciu lat od końca roku kalendarzowego nabycia, a PIT art. 10 ust. 5 wskazuje, że w przypadku spadku okres ten liczy się od nabycia przez spadkodawcę, nie przez Pana. Czy w Pana przypadku termin upłynął, zależy od daty nabycia nieruchomości przez rodziców, której nie znam i nie jestem w stanie ustalić — nie mogę więc rozstrzygnąć, czy podatek jest należny. To nie jest porada podatkowa; w razie wątpliwości proponuję wniosek o interpretację indywidualną (art. 14b Ordynacji podatkowej) lub konsultację z doradcą podatkowym.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 10 ust. 1 pkt 8, PIT art. 10 ust. 5, PIT art. 22 ust. 6d): Nie da się rozstrzygnąć na podstawie podanych informacji. Przy sprzedaży odziedziczonego mieszkania pięcioletni okres liczy się od końca roku kalendarzowego, w którym rodzic nabył lub wybudował nieruchomość, a nie od dnia dziedziczenia (PIT art. 10 ust. 5). Jeżeli sprzedaż nastąpiła po upływie tego okresu, nie mieści się w źródle przychodów z PIT wskazanym w PIT art. 10 ust. 1 pkt 8; jeżeli nastąpiła wcześniej, sprzedaż może podlegać PIT, przy czym koszty ustala się według PIT art. 22 ust. 6d. Brakuje daty nabycia lub wybudowania mieszkania przez rodzica oraz roku sprzedaży, a podane przepisy nie pozwalają ustalić konkretnej kwoty podatku.
**Kontekst:** PIT art. 10, PIT art. 21 ust. 1 pkt 29, PIT art. 22 ust. 6d, Ordynacja art. 70 § 1a pkt 3
**Sędzia 1** (claude-sonnet-5): refusal_ok — System prawidłowo odmówił rozstrzygnięcia z powodu braku daty nabycia przez rodziców, poprawnie przytaczając art. 10 ust. 1 pkt 8 i ust. 5 oraz dodatkowo trafnie wskazując art. 22 ust. 6d dot. kosztów, co jest zgodne z przepisami w kontekście; jedynie pominięto sugestię interpretacji indywidualnej, co nie zmienia poprawności merytorycznej.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-17 (out_of_corpus, oczekiwane: provisions_without_verdict)
**Pytanie:** Czy mój jednoosobowy biznes (sprzedaż online, obrót 180 000 zł w tym roku) musi już zarejestrować się jako podatnik VAT?
**Wzorzec:** Mogę przytoczyć przepisy, które regulują tę kwestię: VAT art. 113 ust. 1 zwalnia od podatku sprzedaż, której wartość nie przekroczyła w poprzednim ani bieżącym roku podatkowym 240 000 zł, a VAT art. 113 ust. 5 wskazuje, że zwolnienie traci moc od czynności, którą limit został przekroczony — obowiązek rejestracji wynika z VAT art. 96 ust. 1. Przy obrocie 180 000 zł limit nie został jeszcze przekroczony, ale nie znam szczegółów Pana działalności (np. czy sprzedaje Pan towary/usługi wyłączone z tego zwolnienia na podstawie art. 113 ust. 13, ani jak liczony jest rok podatkowy w Pana przypadku), więc nie mogę rozstrzygnąć ostatecznie, czy obowiązek rejestracji już powstał. To nie jest porada podatkowa; w razie wątpliwości proponuję konsultację z doradcą podatkowym lub wniosek o interpretację indywidualną.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 113 ust. 1, VAT art. 96 ust. 5): Nie wynika to z samego obrotu 180 000 zł. Jeżeli masz siedzibę działalności w Polsce oraz wartość sprzedaży bez podatku nie przekroczyła 240 000 zł ani w poprzednim, ani w bieżącym roku podatkowym, sprzedaż korzysta ze zwolnienia z VAT (VAT art. 113 ust. 1). Do rozstrzygnięcia brakuje informacji o obrocie w poprzednim roku, rodzaju sprzedawanych towarów lub usług oraz o tym, czy utraciłeś albo zrezygnowałeś ze zwolnienia; w takich przypadkach zgłoszenie rejestracyjne składa się w terminach określonych w VAT art. 96 ust. 5.
**Kontekst:** VAT art. 113 ust. 1, VAT art. 96 ust. 5, VAT art. 113a, VAT art. 96 ust. 4b
**Sędzia 1** (claude-sonnet-5): partial — Odpowiedź poprawnie przytacza art. 113 ust. 1 i wskazuje brak danych o poprzednim roku oraz rodzaju towarów/usług, ale nie wspomina o art. 113 ust. 13 (wyłączenia ze zwolnienia) ani o art. 96 ust. 1 jako podstawie obowiązku rejestracji, a cytowanie art. 96 ust. 5 jako 'terminu zgłoszenia' jest nieco na wyrost przy niepewnym stanie faktycznym.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-18 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy od sprzedaży laptopa prywatnie (jako osoba fizyczna, nieprowadząca działalności) muszę zapłacić VAT i jak długo trzeba przechowywać taką transakcję w ewidencji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 15 ust. 1 wskazuje, że podatnikami VAT są podmioty wykonujące samodzielnie działalność gospodarczą — skoro sprzedaje Pan prywatny przedmiot poza taką działalnością, nie jest Pan podatnikiem VAT z tego tytułu, więc VAT nie wystąpi. Natomiast szczegółowe zasady przechowywania ewidencji/dokumentów przez osoby prywatne nieprowadzące działalności nie są uregulowane w ustawie o VAT (ta reguluje obowiązki podatników VAT, a Pan nim nie jest w tej transakcji) — to wykracza poza mój korpus i nie mogę podać odpowiedzi w tej części.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 111 ust. 1): W podanych przepisach nie ma odpowiedzi, czy prywatna sprzedaż laptopa przez osobę fizyczną nieprowadzącą działalności podlega VAT. VAT art. 111 ust. 1 nakłada obowiązek ewidencji przy zastosowaniu kasy rejestrującej na podatników dokonujących sprzedaży na rzecz osób fizycznych, ale nie rozstrzyga, czy w opisanej sytuacji sprzedawca jest podatnikiem. Przepisy nie określają również, jak długo należy przechowywać taką transakcję w ewidencji.
**Kontekst:** VAT art. 111 ust. 1, VAT art. 110, VAT art. 138c, VAT art. 14 ust. 2, VAT art. 14 ust. 1, VAT art. 146ef
**Sędzia 1** (claude-sonnet-5): partial — System trafnie odmawia odpowiedzi na kwestię przechowywania ewidencji, ale błędnie twierdzi, że przepisy nie rozstrzygają kwestii VAT – art. 15 ust. 1 (dostępny w korpusie wzorca, choć tu nieprzytoczony) wskazuje jasno, że prywatna sprzedaż poza działalnością gospodarczą nie podlega VAT; system nie wykorzystał tej możliwej do udzielenia części odpowiedzi.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-19 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Czy odsetki za zwłokę w podatku są wysokie i czy mogę zapłacić je kartą płatniczą w urzędzie?
**Wzorzec:** Stawka odsetek za zwłokę to suma 200% podstawowej stopy kredytu lombardowego NBP i 2%, nie mniej niż 8% (Ordynacja art. 56 § 1). Co do zapłaty kartą: Ordynacja dopuszcza zapłatę „innym instrumentem płatniczym” za pośrednictwem konta w e-Urzędzie Skarbowym (art. 61 § 1 pkt 2); zasad płacenia kartą bezpośrednio w kasie urzędu w korpusie nie ma.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 56b, Ordynacja art. 55 § 1): W podanych przepisach nie ma konkretnej stawki odsetek, więc nie można na ich podstawie ocenić, czy są „wysokie”; wskazano jedynie, że w określonych przypadkach zaległości w podatku od towarów i usług stosuje się podwyższoną stawkę wynoszącą 150% stawki odsetek za zwłokę (Ordynacja art. 56b). Odsetki wpłaca się bez wezwania organu podatkowego (Ordynacja art. 55 § 1), a przepisy nie odpowiadają na pytanie, czy można zapłacić je kartą płatniczą w urzędzie.
**Kontekst:** Ordynacja art. 53, Ordynacja art. 55, Ordynacja art. 56b, Ordynacja art. 49, Ordynacja art. 76
**Sędzia 1** (claude-sonnet-5): partial — System trafnie wskazał, że w kontekście nie ma podstawowej stawki odsetek (art. 56 nie podano) i prawidłowo odmówił odpowiedzi na część o karcie płatniczej, ale nie zauważył, że art. 56b (150%) dotyczy tylko podwyższonej stawki VAT/akcyza w szczególnych przypadkach, a nie ogólnej oceny 'czy odsetki są wysokie', co może sugerować błędny kontekst odpowiedzi.
**Sędzia 2** (): error — 

## hyde/verify=off · g-ooc-20 (out_of_corpus, oczekiwane: partial_answer)
**Pytanie:** Sprzedaję używany budynek biurowy, który był zasiedlony 5 lat temu — czy ta dostawa jest zwolniona z VAT, i jaką stawkę PCC zapłaci kupujący od tej transakcji?
**Wzorzec:** Część odpowiedzi znajduje się w moim korpusie: VAT art. 43 ust. 1 pkt 10 zwalnia od podatku dostawę budynków, budowli lub ich części, z wyjątkiem dostawy w ramach pierwszego zasiedlenia lub przed nim, oraz dostawy dokonanej w ciągu 2 lat od pierwszego zasiedlenia. Skoro budynek był zasiedlony 5 lat temu (czyli upłynęły więcej niż 2 lata), dostawa korzysta ze zwolnienia z VAT na podstawie tego przepisu. Natomiast kwestia podatku od czynności cywilnoprawnych (PCC), który może obciążać kupującego przy zakupie nieruchomości zwolnionej z VAT, nie jest uregulowana w ustawie o VAT — reguluje ją ustawa o podatku od czynności cywilnoprawnych, która nie jest częścią mojego korpusu, więc nie mogę podać stawki PCC.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 43 ust. 1 pkt 10, VAT art. 43 ust. 10, VAT art. 43 ust. 11): Jeżeli „zasiedlenie” oznacza pierwsze zasiedlenie, a od niego do dostawy upłynęło 5 lat, dostawa budynku jest zwolniona z VAT na podstawie VAT art. 43 ust. 1 pkt 10. Zwolnienie można jednak wyłączyć, jeżeli sprzedający i kupujący są zarejestrowani jako podatnicy VAT czynni oraz złożą zgodne oświadczenie o wyborze opodatkowania zgodnie z VAT art. 43 ust. 10–11. W przekazanych przepisach nie ma regulacji dotyczących stawki PCC, więc nie mogę jej wskazać; pytanie w tym zakresie dotyczy ustawy o podatku od czynności cywilnoprawnych.
**Kontekst:** VAT art. 43 ust. 10, VAT art. 29a ust. 8–9, VAT art. 43 ust. 1 pkt 2–10, VAT art. 43 ust. 11, VAT art. 43 ust. 1 pkt 10a–11
**Sędzia 1** (claude-sonnet-5): correct — Trafnie wskazano zwolnienie z art. 43 ust. 1 pkt 10 i poprawnie dodano informację o możliwości rezygnacji ze zwolnienia (art. 43 ust. 10–11), co jest zgodne z przepisami i nie zmienia sensu odpowiedzi wzorcowej; poprawnie odmówiono wskazania stawki PCC jako spoza korpusu.
**Sędzia 2** (): error — 

## hyde/verify=off · g-op-12 (multi, oczekiwane: answer)
**Pytanie:** Złożyłem korektę deklaracji i zapłaciłem zaległość, ale dopiero po tym, jak dostałem zawiadomienie o zamiarze wszczęcia kontroli. Czy przysługuje mi obniżona stawka odsetek za zwłokę?
**Wzorzec:** Nie. Obniżona stawka odsetek (50% stawki odsetek za zwłokę) przysługuje przy korekcie złożonej w ciągu 6 miesięcy od terminu złożenia deklaracji i zapłacie zaległości w ciągu 7 dni od korekty (art. 56a § 1), ale nie stosuje się jej do korekty złożonej po doręczeniu zawiadomienia o zamiarze wszczęcia kontroli podatkowej (art. 56a § 3 pkt 1).
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 56a § 1, Ordynacja art. 56a § 3 pkt 1): Nie. Obniżonej stawki odsetek za zwłokę nie stosuje się do korekty deklaracji złożonej po doręczeniu zawiadomienia o zamiarze wszczęcia kontroli podatkowej, nawet jeśli zaległość została zapłacona po złożeniu korekty.
**Kontekst:** Ordynacja art. 56a, Ordynacja art. 56b, Ordynacja art. 57, Ordynacja art. 20zm
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem – poprawnie wskazuje, że obniżona stawka nie przysługuje po doręczeniu zawiadomienia o kontroli, z prawidłowym cytatem art. 56a §3 pkt 1; brak błędów merytorycznych.
**Sędzia 2** (): error — 

## simple/verify=off · g-vat-25 (colloquial, oczekiwane: answer)
**Pytanie:** Otwieram warsztat krawiecki i będę podatnikiem VAT (nie korzystam ze zwolnienia). Czy muszę się zgłosić do urzędu skarbowego przed pierwszą sprzedażą, czy mogę to zrobić później, np. po miesiącu działania?
**Wzorzec:** Musi Pani złożyć naczelnikowi urzędu skarbowego zgłoszenie rejestracyjne przed dniem wykonania pierwszej czynności opodatkowanej (np. pierwszej sprzedaży) — zgłoszenia po fakcie nie przewidziano jako zgodnego z ustawą terminu.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 96 ust. 5 pkt 1): Tak. Jeżeli rozpoczynasz sprzedaż opodatkowaną, musisz złożyć zgłoszenie rejestracyjne przed dniem dokonania pierwszej sprzedaży towaru lub usługi, innej niż wskazana w przepisie jako zwolniona. Nie możesz więc odłożyć zgłoszenia do czasu po miesiącu działalności.
**Kontekst:** VAT art. 96 ust. 5, VAT art. 33b, VAT art. 33a, VAT art. 96 ust. 10c, VAT art. 48
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje obowiązek rejestracji przed dniem pierwszej sprzedaży opodatkowanej na podstawie art. 96 ust. 5 pkt 1, zgodnie z wzorcem, bez dodawania treści spoza kontekstu.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje obowiązek złożenia zgłoszenia rejestracyjnego przed pierwszą sprzedażą inną niż zwolniona oraz słusznie wyklucza dokonanie tego dopiero po miesiącu działalności. Wynika to bezpośrednio z art. 96 ust. 5 pkt 1 ustawy o VAT.

## hybrid/verify=off · g-vat-19 (multi, oczekiwane: answer)
**Pytanie:** Mój klient nie zapłacił mi za fakturę wystawioną 2 lata temu i minęło już 90 dni od terminu płatności. Czy mogę skorygować podatek należny z tytułu tej nieściągalnej wierzytelności?
**Wzorzec:** Tak, co do zasady — nieściągalność uważa się za uprawdopodobnioną po 90 dniach od terminu płatności (art. 89a ust. 1a), a korekta jest możliwa, o ile wierzyciel na dzień poprzedzający złożenie korygującej deklaracji jest zarejestrowanym podatnikiem VAT czynnym oraz od wystawienia faktury nie upłynęły 3 lata, licząc od końca roku, w którym ją wystawiono (art. 89a ust. 2 pkt 3 lit. a i pkt 5). Przy fakturze wystawionej 2 lata temu warunek 3-letni jest jeszcze spełniony.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 89a ust. 1, VAT art. 89a ust. 1a, VAT art. 89a ust. 2 pkt 3 lit. a, VAT art. 89a ust. 2 pkt 5, VAT art. 89a ust. 2a, VAT art. 89a ust. 3, VAT art. 89a ust. 5): Możesz skorygować podstawę opodatkowania i podatek należny, jeżeli nieściągalność wierzytelności jest uprawdopodobniona, czyli wierzytelność nie została uregulowana ani zbyta w ciągu 90 dni od upływu terminu płatności, oraz spełnione są pozostałe warunki. W szczególności na dzień poprzedzający złożenie deklaracji musisz być podatnikiem zarejestrowanym jako podatnik VAT czynny, a od wystawienia faktury nie mogą upłynąć 3 lata, licząc od końca roku, w którym ją wystawiono; do dnia złożenia deklaracji wierzytelność nie może zostać uregulowana ani zbyta. Korekty dokonuje się w rozliczeniu za okres, w którym nieściągalność uznaje się za uprawdopodobnioną, a o korekcie informuje się właściwego naczelnika urzędu skarbowego w deklaracji. Jeżeli klient nie jest podatnikiem VAT czynnym, korekta wymaga dodatkowo spełnienia jednego z warunków wskazanych w VAT art. 89a ust. 2a; na podstawie podanych informacji nie da się stwierdzić, czy wszystkie warunki są spełnione.
**Kontekst:** VAT art. 89b, VAT art. 89a, VAT art. 19a ust. 7
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem, zawiera wszystkie kluczowe warunki (90 dni, status VAT czynny wierzyciela, termin 3 lat) i prawidłowo wskazuje, że przy fakturze z 2 lat warunek 3-letni jest spełniony; dodatkowo poprawnie wspomina o art. 89a ust. 2a dla dłużników niebędących podatnikami VAT czynnymi, co jest zgodne z kontekstem.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje przesłankę 90 dni, warunek czynnego VAT po stronie wierzyciela, limit 3 lat oraz wymóg braku uregulowania lub zbycia do dnia złożenia deklaracji. Trafnie uwzględnia też dodatkowe warunki z art. 89a ust. 2a dla dłużnika niebędącego czynnym podatnikiem VAT.

## hybrid/verify=off · g-ooc-16 (out_of_corpus, oczekiwane: provisions_without_verdict)
**Pytanie:** Sprzedałem mieszkanie, które odziedziczyłem po rodzicach 4 lata temu. Czy zapłacę podatek PIT od tej sprzedaży w moim przypadku?
**Wzorzec:** Mogę przytoczyć przepisy, które regulują tę kwestię: PIT art. 10 ust. 1 pkt 8 lit. a wiąże obowiązek podatkowy ze zbyciem nieruchomości przed upływem pięciu lat od końca roku kalendarzowego nabycia, a PIT art. 10 ust. 5 wskazuje, że w przypadku spadku okres ten liczy się od nabycia przez spadkodawcę, nie przez Pana. Czy w Pana przypadku termin upłynął, zależy od daty nabycia nieruchomości przez rodziców, której nie znam i nie jestem w stanie ustalić — nie mogę więc rozstrzygnąć, czy podatek jest należny. To nie jest porada podatkowa; w razie wątpliwości proponuję wniosek o interpretację indywidualną (art. 14b Ordynacji podatkowej) lub konsultację z doradcą podatkowym.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi, czy sprzedaż odziedziczonego mieszkania podlega opodatkowaniu PIT ani jak ustalać okres posiadania nieruchomości. Do rozstrzygnięcia potrzebne są przepisy dotyczące odpłatnego zbycia nieruchomości w ustawie o PIT.
**Kontekst:** PIT art. 30df, PIT art. 42f, PIT art. 22 ust. 1h, PIT art. 27f ust. 10, PIT art. 41 ust. 4h
**Sędzia 1** (claude-sonnet-5): refusal_ok — Kontekst systemu faktycznie nie zawiera art. 10 ust. 1 pkt 8 i art. 10 ust. 5 PIT regulujących to zagadnienie, więc odmowa była zasadna i zgodna z dostarczonymi przepisami, choć odpowiedź mogłaby wskazać konieczność konsultacji z doradcą/interpretacji indywidualnej.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W przekazanym kontekście nie ma art. 10 ust. 1 pkt 8 ani art. 10 ust. 5 ustawy o PIT, które regulują sprzedaż nieruchomości i liczenie terminu przy spadku. System prawidłowo odmówił rozstrzygnięcia i nie dopowiedział treści spoza kontekstu.

## hybrid/verify=off · g-ooc-06 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaką stawkę podatku od spadków i darowizn płaci się przy darowiźnie od rodzica dla dziecka?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Stawki i zwolnienia w podatku od spadków i darowizn, w tym dla najbliższej rodziny, reguluje ustawa o podatku od spadków i darowizn, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na pytanie o stawkę podatku od spadków i darowizn przy darowiźnie od rodzica dla dziecka.
**Kontekst:** PIT art. 27f ust. 4, PIT art. 22 ust. 6d, PIT art. 26 ust. 6, PIT art. 27f ust. 10, PIT art. 23 ust. 1 pkt 10–14
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił odpowiedzi, wskazując brak informacji w kontekście; jedynym niedociągnięciem jest brak wskazania, że temat reguluje ustawa o podatku od spadków i darowizn, ale to nie zmienia poprawności samej odmowy.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił, ponieważ przekazane przepisy nie określają stawki podatku od spadków i darowizn dla darowizny od rodzica dla dziecka. Odpowiedź nie dopowiada informacji spoza kontekstu.

## hybrid/verify=off · g-op-10 (colloquial, oczekiwane: answer)
**Pytanie:** Dostałem decyzję z urzędu skarbowego, z którą się nie zgadzam — ile czasu mam na złożenie odwołania i do kogo je składam?
**Wzorzec:** Odwołanie wnosi się w terminie 14 dni od dnia doręczenia decyzji, składając je do właściwego organu odwoławczego za pośrednictwem organu podatkowego, który wydał decyzję.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 223 § 1–2, Ordynacja art. 222): Odwołanie należy wnieść w terminie 14 dni od dnia doręczenia decyzji. Składa się je do właściwego organu odwoławczego za pośrednictwem organu podatkowego, który wydał decyzję. Odwołanie powinno zawierać zarzuty przeciw decyzji, określać istotę i zakres żądania oraz wskazywać dowody uzasadniające to żądanie.
**Kontekst:** Ordynacja art. 223, Ordynacja art. 227, Ordynacja art. 233, Ordynacja art. 291, Ordynacja art. 222
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zgodna z wzorcem (termin 14 dni, organ odwoławczy za pośrednictwem organu wydającego decyzję), dodatkowa informacja o wymogach formalnych odwołania jest poprawna i wynika z art. 222 w kontekście.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje termin 14 dni od doręczenia decyzji oraz wniesienie odwołania do organu odwoławczego za pośrednictwem organu, który wydał decyzję. Dodatkowa informacja o wymaganej treści odwołania wynika wprost z art. 222 Ordynacji.

## simple/verify=off · g-vat-10 (fact, oczekiwane: answer)
**Pytanie:** W którym momencie co do zasady powstaje obowiązek podatkowy w VAT?
**Wzorzec:** Obowiązek podatkowy powstaje z chwilą dokonania dostawy towarów lub wykonania usługi, z zastrzeżeniem wyjątków wskazanych w ust. 1a, 1b, 5 i 7–11 oraz innych wskazanych przepisów.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 19a ust. 1, VAT art. 19a ust. 1a, VAT art. 19a ust. 1b, VAT art. 19a ust. 5 pkt 1–2, VAT art. 19a ust. 6): Co do zasady obowiązek podatkowy w VAT powstaje z chwilą dokonania dostawy towarów lub wykonania usługi (VAT art. 19a ust. 1). Przepis przewiduje wyjątki, między innymi dla transferu bonu jednego przeznaczenia, dostaw dokonywanych na rzecz podatnika ułatwiającego dostawy oraz przypadków otrzymania zapłaty, dotacji, subwencji lub innych dopłat wskazanych w przepisie (VAT art. 19a ust. 1a, 1b i 5 pkt 1–2).
**Kontekst:** VAT art. 19a ust. 1, VAT art. 19a ust. 1a, VAT art. 19a ust. 5 pkt 1–2, VAT art. 19a ust. 6, VAT art. 19a ust. 1b
**Sędzia 1** (claude-sonnet-5): correct — Główna zasada podana prawidłowo, wyjątki opisane zgodnie z przepisami w kontekście; system nie dodał faktów spoza podanych artykułów.
**Sędzia 2** (gpt-5.6-terra): correct — System prawidłowo wskazuje zasadę z art. 19a ust. 1 VAT: obowiązek podatkowy powstaje przy dostawie towarów lub wykonaniu usługi. Wspomniane wyjątki są zgodne z przepisami dostępnymi w kontekście.

## simple/verify=off · g-op-01 (fact, oczekiwane: answer)
**Pytanie:** Po jakim okresie przedawnia się zobowiązanie podatkowe, licząc od terminu płatności podatku?
**Wzorzec:** Zobowiązanie podatkowe przedawnia się z upływem 5 lat, licząc od końca roku kalendarzowego, w którym upłynął termin płatności podatku.
**Odpowiedź** (odmowa=False; cytaty: Ordynacja art. 70 § 1, Ordynacja art. 70 § 1a pkt 3, Ordynacja art. 70 § 1b): Co do zasady zobowiązanie podatkowe przedawnia się z upływem 5 lat, licząc od końca roku kalendarzowego, w którym upłynął termin płatności podatku, a nie bezpośrednio od dnia terminu płatności (Ordynacja art. 70 § 1). Dla niektórych zobowiązań podatników podatku dochodowego od osób prawnych obowiązują szczególne zasady określone w Ordynacja art. 70 § 1a pkt 3 i Ordynacja art. 70 § 1b.
**Kontekst:** Ordynacja art. 70 § 1b, Ordynacja art. 70 § 1, Ordynacja art. 64, Ordynacja art. 47, Ordynacja art. 70 § 1a pkt 3
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź prawidłowo podaje zasadę 5 lat od końca roku kalendarzowego terminu płatności (art. 70 §1) i zasadnie dodaje informację o szczególnych wyjątkach dla CIT, co nie zmienia sensu głównej tezy, a wszystko wynika z przepisów w kontekście.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź poprawnie podaje ogólną zasadę z art. 70 § 1: 5 lat od końca roku kalendarzowego, w którym upłynął termin płatności. Wzmianka o szczególnych zasadach dla wskazanych zobowiązań CIT wynika z przytoczonych art. 70 § 1a pkt 3 i § 1b.

## simple/verify=off · g-vat-19 (multi, oczekiwane: answer)
**Pytanie:** Mój klient nie zapłacił mi za fakturę wystawioną 2 lata temu i minęło już 90 dni od terminu płatności. Czy mogę skorygować podatek należny z tytułu tej nieściągalnej wierzytelności?
**Wzorzec:** Tak, co do zasady — nieściągalność uważa się za uprawdopodobnioną po 90 dniach od terminu płatności (art. 89a ust. 1a), a korekta jest możliwa, o ile wierzyciel na dzień poprzedzający złożenie korygującej deklaracji jest zarejestrowanym podatnikiem VAT czynnym oraz od wystawienia faktury nie upłynęły 3 lata, licząc od końca roku, w którym ją wystawiono (art. 89a ust. 2 pkt 3 lit. a i pkt 5). Przy fakturze wystawionej 2 lata temu warunek 3-letni jest jeszcze spełniony.
**Odpowiedź** (odmowa=True; cytaty: VAT art. 89b): W podanych przepisach nie ma podstawy do stwierdzenia, czy wierzyciel może skorygować podatek należny z tytułu nieściągalnej wierzytelności. VAT art. 89b dotyczy obowiązku dłużnika do korekty odliczonego podatku naliczonego po upływie 90 dni od terminu płatności, a nie korekty podatku należnego przez wierzyciela; wynik zależałby od przepisów dotyczących wierzyciela, których tu nie podano.
**Kontekst:** VAT art. 89b, Ordynacja art. 14za, Ordynacja art. 299f, Ordynacja art. 14f
**Sędzia 1** (claude-sonnet-5): refusal_ok — Kontekst systemu nie zawiera art. 89a VAT (podstawy do korekty podatku należnego przez wierzyciela) – tylko art. 89b dotyczący dłużnika, więc słusznie odmówiono odpowiedzi, nie fabrykując treści art. 89a.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — W kontekście jest wyłącznie art. 89b VAT dotyczący korekty podatku naliczonego przez dłużnika, a brak art. 89a regulującego ulgę po stronie wierzyciela. Odmowa udzielenia odpowiedzi o korekcie podatku należnego przez wierzyciela była więc właściwa i oparta wyłącznie na dostępnych przepisach.

## hybrid/verify=off · g-vat-09 (fact, oczekiwane: answer)
**Pytanie:** Jak długo podatnik musi przechowywać ewidencje i faktury związane z rozliczaniem VAT?
**Wzorzec:** Podatnicy są obowiązani przechowywać ewidencje oraz wszystkie dokumenty, w szczególności faktury, związane z rozliczaniem VAT do czasu upływu terminu przedawnienia zobowiązania podatkowego (z zastrzeżeniami wymienionymi w art. 112).
**Odpowiedź** (odmowa=False; cytaty: VAT art. 112, VAT art. 112a ust. 1, VAT art. 109b ust. 7): Co do zasady ewidencje prowadzone dla celów rozliczania VAT oraz dokumenty, w szczególności faktury, podatnik przechowuje do upływu terminu przedawnienia zobowiązania podatkowego; faktury należy przechowywać w podziale na okresy rozliczeniowe, z zapewnieniem ich autentyczności, integralności i czytelności (VAT art. 112, VAT art. 112a ust. 1). Dla ewidencji czynności objętych VAT art. 109b obowiązuje szczególny okres 10 lat od zakończenia roku podatkowego, w którym dokonano dostawy lub wykonano usługę (VAT art. 109b ust. 7). W podanych przepisach nie ma długości terminu przedawnienia zobowiązania podatkowego, więc nie można wskazać liczby lat dla ogólnego obowiązku przechowywania ewidencji i faktur.
**Kontekst:** VAT art. 112, VAT art. 109b, VAT art. 112a, VAT art. 116 ust. 10, VAT art. 116 ust. 11
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź zawiera główną tezę zgodną z wzorcem (termin przedawnienia zobowiązania podatkowego, art. 112 i 112a) oraz dodatkowo poprawnie wskazuje wyjątek z art. 109b ust. 7, który wzorzec jedynie ogólnie zastrzega. System trafnie zauważa, że sam termin przedawnienia nie jest zdefiniowany w dostarczonych przepisach, co jest zgodne z kontekstem.
**Sędzia 2** (gpt-5.6-terra): correct — Prawidłowo wskazano ogólną zasadę przechowywania ewidencji i dokumentów VAT do upływu przedawnienia zobowiązania podatkowego. Trafnie dodano szczególny 10-letni okres dla ewidencji z art. 109b ust. 1 oraz wymogi dotyczące przechowywania faktur z art. 112a.

## hybrid/verify=off · g-vat-02 (fact, oczekiwane: answer)
**Pytanie:** Od jakiej kwoty faktury za towary z załącznika nr 15 do ustawy podatnik jest obowiązany zastosować mechanizm podzielonej płatności (split payment)?
**Wzorzec:** Przy płatności za towary lub usługi z załącznika nr 15 do ustawy, udokumentowanej fakturą, w której kwota należności ogółem przekracza 15 000 zł (lub równowartość w walucie obcej), podatnik jest obowiązany zastosować mechanizm podzielonej płatności.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 108a ust. 1a): Podatnik jest obowiązany zastosować mechanizm podzielonej płatności, gdy faktura za towary lub usługi wymienione w załączniku nr 15 dokumentuje należność ogółem przekraczającą 15 000 zł albo jej równowartość w walucie obcej. Obowiązek dotyczy płatności za nabyte towary lub usługi, a nie samego wystawienia faktury.
**Kontekst:** VAT art. 108a ust. 1a, VAT art. 106e ust. 13, VAT art. 108a ust. 1, VAT art. 108a ust. 7, VAT art. 108a ust. 1b
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie podaje próg 15 000 zł (lub równowartość w walucie obcej) dla faktur z załącznika nr 15, zgodnie z art. 108a ust. 1a, i dodaje zgodne z przepisem wyjaśnienie, że obowiązek dotyczy płatności, nie samego wystawienia faktury.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje próg przekraczający 15 000 zł (lub równowartość w walucie obcej) dla towarów lub usług z załącznika nr 15. Trafnie doprecyzowuje też, że obowiązek dotyczy dokonywania płatności, zgodnie z art. 108a ust. 1a.

## hybrid/verify=off · g-vat-05 (fact, oczekiwane: answer)
**Pytanie:** W jakim terminie podatnik VAT rozliczający się miesięcznie musi wpłacić podatek na rachunek urzędu skarbowego?
**Wzorzec:** Podatnicy są obowiązani, bez wezwania naczelnika urzędu skarbowego, wpłacać podatek za okresy miesięczne w terminie do 25. dnia miesiąca następującego po miesiącu, w którym powstał obowiązek podatkowy.
**Odpowiedź** (odmowa=False; cytaty: VAT art. 103 ust. 1): Podatnik VAT rozliczający się miesięcznie musi obliczyć i wpłacić podatek bez wezwania naczelnika urzędu skarbowego do 25. dnia miesiąca następującego po miesiącu, w którym powstał obowiązek podatkowy, z zastrzeżeniem wyjątków wskazanych w przepisie. 
**Kontekst:** VAT art. 103 ust. 3, VAT art. 103 ust. 1, VAT art. 87 ust. 2, VAT art. 103 ust. 2, VAT art. 108b ust. 1a–3
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź wiernie oddaje treść art. 103 ust. 1 (termin do 25. dnia miesiąca następującego, bez wezwania), zgodnie z wzorcem; dodatkowe zastrzeżenie o wyjątkach jest prawidłowym elementem przepisu, nie zmienia sensu.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje termin do 25. dnia następnego miesiąca, obowiązek wpłaty bez wezwania oraz odnosi go do miesiąca powstania obowiązku podatkowego. Zastrzeżenie wyjątków jest zgodne z art. 103 ust. 1.

## hybrid/verify=off · g-pit-07 (fact, oczekiwane: answer)
**Pytanie:** Jaką stawkę podatku dochodowego stosuje się do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia?
**Wzorzec:** Podatek dochodowy od dochodu z odpłatnego zbycia nieruchomości i praw określonych w art. 10 ust. 1 pkt 8 lit. a–c wynosi 19% podstawy obliczenia podatku.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 30e ust. 1): Do dochodu z odpłatnego zbycia nieruchomości, który nie korzysta ze zwolnienia, stosuje się podatek dochodowy według stawki 19% podstawy obliczenia podatku (PIT art. 30e ust. 1).
**Kontekst:** PIT art. 21 ust. 1 pkt 29, PIT art. 21 ust. 1 pkt 131–133, PIT art. 21 ust. 1 pkt 29aa–29ab, PIT art. 30e
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź wskazuje poprawną stawkę 19% z poprawnym przepisem (art. 30e ust. 1), zgodnie z wzorcem.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje stawkę 19% podstawy obliczenia podatku, zgodnie z art. 30e ust. 1 PIT. Twierdzenie w całości wynika z przepisu w kontekście.

## simple/verify=off · g-ooc-10 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Ile kosztuje opłata skarbowa za pełnomocnictwo złożone w urzędzie skarbowym?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa), nie ma odpowiedzi na to pytanie. Wysokość opłaty skarbowej za pełnomocnictwo reguluje ustawa o opłacie skarbowej, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi dotyczącej opłaty skarbowej za pełnomocnictwo złożone w urzędzie skarbowym.
**Kontekst:** Ordynacja art. 14z, Ordynacja art. 119zfv, Ordynacja art. 267, Ordynacja art. 119zc, Ordynacja art. 269
**Sędzia 1** (claude-sonnet-5): refusal_ok — System prawidłowo odmówił, wskazując brak odpowiedzi w dostępnych przepisach; nie wskazał jednak (jak wzorzec) konkretnej ustawy o opłacie skarbowej, co jest drobnym niedociągnięciem, ale nie wpływa na poprawność odmowy.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił, ponieważ podane przepisy nie określają opłaty skarbowej za pełnomocnictwo. Nie dodał informacji spoza kontekstu.

## hybrid/verify=off · g-ooc-03 (out_of_corpus, oczekiwane: refuse_with_pointer)
**Pytanie:** Jaka jest stawka podatku CIT dla małych podatników w 2026 roku?
**Wzorzec:** W przepisach, które mam (VAT, PIT, Ordynacja podatkowa — stan na 2026-08-26 / 2026-04-01 / 2026-04-21), nie ma odpowiedzi na to pytanie. Stawki podatku dochodowego od osób prawnych (CIT), w tym stawkę dla małych podatników, reguluje ustawa o podatku dochodowym od osób prawnych, która nie jest częścią mojego korpusu.
**Odpowiedź** (odmowa=True; cytaty: ): W przepisach, które mam, nie ma odpowiedzi na pytanie o stawkę podatku CIT dla małych podatników w 2026 roku.
**Kontekst:** VAT art. 99 ust. 3, PIT art. 26ea, PIT art. 26hd, PIT art. 26he, PIT art. 44 ust. 6h
**Sędzia 1** (claude-sonnet-5): refusal_ok — System poprawnie odmówił, bo stawka CIT dla małych podatników nie znajduje się w dostępnych przepisach (VAT/PIT/Ordynacja); nie wskazał jednak, że regulacja ta jest w ustawie o CIT, co byłoby pożądanym dodatkiem, ale nie jest błędem.
**Sędzia 2** (gpt-5.6-terra): refusal_ok — System prawidłowo odmówił, ponieważ w przekazanym kontekście nie ma przepisu określającego stawkę CIT dla małych podatników. Nie dopowiedział żadnych informacji spoza korpusu.

## simple/verify=off · g-pit-10 (multi, oczekiwane: answer)
**Pytanie:** Czy podatnik opodatkowany podatkiem liniowym (art. 30c) może rozliczyć się wspólnie z małżonkiem na zasadach art. 6?
**Wzorzec:** Nie. Wspólne opodatkowanie małżonków (art. 6 ust. 2) nie ma zastosowania, jeśli chociażby jeden z małżonków stosuje opodatkowanie podatkiem liniowym na podstawie art. 30c, w zakresie osiągniętych w roku podatkowym przychodów objętych tym sposobem opodatkowania.
**Odpowiedź** (odmowa=False; cytaty: PIT art. 6 ust. 2, PIT art. 6 ust. 8 pkt 1 lit. a): Nie. Wspólne opodatkowanie małżonków na zasadach art. 6 ust. 2 nie ma zastosowania, jeżeli chociażby jeden z małżonków stosuje przepisy art. 30c w zakresie wskazanym w tym przepisie (PIT art. 6 ust. 8 pkt 1 lit. a).
**Kontekst:** PIT art. 6 ust. 2, Ordynacja art. 29, PIT art. 6 ust. 8, PIT art. 26hb, PIT art. 27f ust. 2d
**Sędzia 1** (claude-sonnet-5): correct — Odpowiedź poprawnie wskazuje brak możliwości wspólnego rozliczenia i prawidłowo cytuje podstawę prawną (art. 6 ust. 8 pkt 1 lit. a), zgodnie ze wzorcem.
**Sędzia 2** (gpt-5.6-terra): correct — Odpowiedź prawidłowo wskazuje wyłączenie wspólnego opodatkowania, gdy co najmniej jeden z małżonków stosuje art. 30c, zgodnie z art. 6 ust. 8 pkt 1 lit. a PIT. Jest oparta wyłącznie na przepisach z kontekstu.
