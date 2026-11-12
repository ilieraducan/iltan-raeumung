# Builds ru/index.html and ro/index.html from the German index.html.
# Run from repo root: python3 tools/i18n.py
import re, json, os

T = {
 'ru': {
  'Stade · Buxtehude · Hamburg': 'Штаде · Букстехуде · Гамбург',
  'Entrümpelung zum': 'Освобождение помещений по',
  'Festpreis': 'фиксированной цене',
  ', besenrein übergeben.': ', сдаём чисто убранным.',
  'Wohnungen, Häuser, Keller, Dachböden und Gewerbeflächen. Schicken Sie uns ein paar Fotos – Sie bekommen innerhalb von 24 Stunden ein verbindliches Angebot.': 'Квартиры, дома, подвалы, чердаки и коммерческие помещения. Пришлите нам несколько фото — в течение 24 часов вы получите точное предложение.',
  'Fotos per WhatsApp senden': 'Отправить фото в WhatsApp',
  'Kosten schätzen': 'Оценить объём',
  'Container für Restmüll': 'Контейнер для мусора',
  'Bei größeren Räumungen bestellen wir einen Container bei einem zugelassenen Entsorgungsfachbetrieb. Der Müll wird dort fachgerecht sortiert und verwertet – Sie haben keinen Aufwand.': 'При больших объёмах заказываем контейнер у лицензированной фирмы по утилизации. Там мусор правильно сортируют и перерабатывают — вам ни о чём не нужно беспокоиться.',
  '💬 Schreiben Sie uns per WhatsApp – unser Mitarbeiter ruft Sie zurück.': '💬 Напишите нам в WhatsApp — наш сотрудник вам перезвонит.',
  'WhatsApp – wir rufen zurück': 'WhatsApp — перезвоним',
  '🎥 Per Video schätzen': '🎥 Оценка по видео',
  'Genauer: Raum per Video scannen': 'Точнее: оценка по видео',
  'Kostenlose Besichtigung vor Ort oder per Foto': 'Бесплатный осмотр на месте или по фото',
  'Festpreis ohne versteckte Kosten': 'Фиксированная цена без скрытых доплат',
  'Fachgerechte Entsorgung und Recycling': 'Правильная утилизация и переработка',
  'Wertanrechnung für verwertbare Gegenstände': 'Зачёт стоимости пригодных вещей',
  'Leistungen': 'Услуги',
  'Wir räumen, was Sie nicht mehr brauchen': 'Вывезем всё, что вам больше не нужно',
  'Wohnungsentrümpelung': 'Освобождение квартир',
  'Komplette Räumung von Mietwohnungen und Eigentum – auch kurzfristig vor der Wohnungsübergabe.': 'Полное освобождение съёмных и собственных квартир — в том числе срочно перед сдачей квартиры.',
  'Haushaltsauflösung': 'Ликвидация домашнего хозяйства',
  'Nach Umzug ins Pflegeheim oder einem Todesfall. Ruhig, respektvoll, auf Wunsch ohne Ihre Anwesenheit.': 'После переезда в дом престарелых или смерти близкого. Спокойно, уважительно, по желанию без вашего присутствия.',
  'Keller &amp; Dachboden': 'Подвал и чердак',
  'Schnell wieder Platz: Kellerabteile, Dachböden, Garagen und Gartenhäuser.': 'Быстро освободим место: подвалы, чердаки, гаражи и садовые домики.',
  'Messie-Wohnungen': 'Захламлённые квартиры',
  'Diskrete Räumung stark vermüllter Wohnungen, mit Grundreinigung nach Absprache.': 'Деликатная расчистка сильно захламлённых квартир, с генеральной уборкой по договорённости.',
  'Gewerbe &amp; Büro': 'Офисы и предприятия',
  'Büros, Lager und Ladenflächen – Möbel, Akten, Elektrogeräte, Regale.': 'Офисы, склады и магазины — мебель, документы, техника, стеллажи.',
  'Sperrmüll-Abholung': 'Вывоз крупногабаритного мусора',
  'Einzelne Möbel, Matratzen oder Elektrogeräte holen wir direkt bei Ihnen ab.': 'Заберём отдельную мебель, матрасы или бытовую технику прямо у вас.',
  'Ablauf': 'Как мы работаем',
  "So einfach geht's": 'Всё очень просто',
  'Fotos oder Termin': 'Фото или осмотр',
  'Fotos per WhatsApp schicken oder eine kostenlose Besichtigung vereinbaren.': 'Пришлите фото в WhatsApp или договоритесь о бесплатном осмотре.',
  'Festpreis-Angebot': 'Фиксированная цена',
  'Innerhalb von 24 Stunden erhalten Sie ein schriftliches Angebot.': 'В течение 24 часов вы получите письменное предложение.',
  'Räumung': 'Вывоз',
  'Wir kommen zum Wunschtermin, tragen alles raus und entsorgen fachgerecht.': 'Приезжаем в удобный день, всё выносим и правильно утилизируем.',
  'Übergabe': 'Сдача',
  'Die Räume werden besenrein übergeben – bereit für Vermieter oder Käufer.': 'Помещение сдаём чисто выметенным — готовым для арендодателя или покупателя.',
  'Preise': 'Цены',
  'Festpreis statt Stundenlohn': 'Фиксированная цена вместо почасовой оплаты',
  'Besichtigung': 'Осмотр',
  'kostenlos': 'бесплатно',
  'Angebot per Foto': 'Предложение по фото',
  'in 24 Std.': 'за 24 ч',
  'Arbeit, Transport, Entsorgung': 'Работа, транспорт, утилизация',
  'im Festpreis': 'входят в цену',
  'Wertanrechnung': 'Зачёт стоимости вещей',
  'möglich': 'возможен',
  'Versteckte Kosten': 'Скрытые доплаты',
  'keine': 'нет',
  'Der Preis hängt von Menge, Etage und Zugang ab. Mit dem Rechner schätzen Sie die Menge – den verbindlichen Festpreis nennen wir Ihnen nach Fotos oder Besichtigung.': 'Цена зависит от объёма, этажа и подъезда. Калькулятор поможет оценить объём, а точную фиксированную цену мы назовём по фото или после осмотра.',
  'Objekt': 'Объект',
  'Wohnung': 'Квартира',
  'Haus': 'Дом',
  'Keller / Dachboden': 'Подвал / чердак',
  'Gewerbe': 'Предприятие',
  'Fläche (m²)': 'Площадь (м²)',
  'Wie voll ist es?': 'Насколько заставлено?',
  'Wenig': 'Немного',
  'Normal': 'Средне',
  'Sehr voll': 'Очень много',
  'Etage ohne Aufzug': 'Этаж без лифта',
  'Erdgeschoss / mit Aufzug': 'Первый этаж / есть лифт',
  '1. Etage': '2-й этаж',
  '2. Etage': '3-й этаж',
  '3. Etage oder höher': '4-й этаж и выше',
  'Geschätzte Menge Räumgut': 'Примерный объём вывоза',
  'entspricht etwa 2 Transporterladungen · unverbindliche Schätzung': 'рейсов фургона: ~2 · предварительная оценка',
  'Festpreis per WhatsApp anfragen': 'Узнать цену в WhatsApp',
  'Einsatzgebiet': 'Где мы работаем',
  'Stade, Hamburg und rund 100 km Umkreis': 'Штаде, Гамбург и около 100 км вокруг',
  'Häufige Fragen': 'Частые вопросы',
  'Gut zu wissen': 'Полезно знать',
  'Wie schnell können Sie räumen?': 'Как быстро вы можете всё вывезти?',
  'In der Regel innerhalb von 3–7 Tagen nach Auftrag, in dringenden Fällen auch kurzfristiger. Eine normale Wohnung räumen wir meist an einem Tag.': 'Обычно в течение 3–7 дней после заказа, в срочных случаях быстрее. Обычную квартиру мы, как правило, освобождаем за один день.',
  'Muss ich bei der Räumung dabei sein?': 'Нужно ли мне присутствовать?',
  'Nein. Sie können uns den Schlüssel übergeben. Nach der Räumung schicken wir Ihnen Fotos der leeren Räume.': 'Нет. Можете передать нам ключ. После работы мы пришлём фото пустых помещений.',
  'Was passiert mit brauchbaren Möbeln?': 'Что будет с хорошей мебелью?',
  'Verwertbare Gegenstände rechnen wir auf den Preis an oder geben sie an soziale Einrichtungen weiter. Der Rest wird getrennt und fachgerecht entsorgt.': 'Пригодные вещи мы засчитываем в цену или передаём в социальные организации. Остальное сортируем и правильно утилизируем.',
  'Ist der Preis wirklich fest?': 'Цена действительно фиксированная?',
  'Ja. Nach der Besichtigung oder anhand Ihrer Fotos nennen wir einen Festpreis. Wenn nichts Unvorhergesehenes dazukommt, zahlen Sie genau diesen Betrag.': 'Да. После осмотра или по вашим фото мы называем фиксированную цену. Если не появится ничего непредвиденного, вы платите ровно эту сумму.',
  'Wie bezahle ich?': 'Как оплатить?',
  'Nach der Übergabe per Überweisung auf Rechnung. Für Privatkunden ist der Arbeitsanteil als haushaltsnahe Dienstleistung steuerlich absetzbar.': 'После сдачи помещения — переводом по счёту. Частные клиенты могут вычесть стоимость работы из налогов как бытовую услугу (haushaltsnahe Dienstleistung).',
  'Jetzt kostenloses Angebot holen': 'Получите бесплатное предложение',
  'Schicken Sie 3–5 Fotos der Räume per WhatsApp. Wir melden uns noch am selben Tag mit einem Festpreis.': 'Пришлите 3–5 фото помещений в WhatsApp. В тот же день мы ответим с фиксированной ценой.',
  'WhatsApp schreiben': 'Написать в WhatsApp',
  'Telefon / WhatsApp · Deutsch': 'Телефон / WhatsApp · на немецком',
  'Erreichbar': 'Время работы',
  'Mo–Sa, 8–19 Uhr': 'Пн–Сб, 8–19 ч',
  '© 2026 Iltan Räumung · Entrümpelung in Stade &amp; Hamburg': '© 2026 Iltan Räumung · освобождение помещений в Штаде и Гамбурге',
  'Anrufen': 'Позвонить',
  'Unsere Zusagen': 'Наши гарантии',
  'Kostenrechner': 'Калькулятор',
  'Schnellkontakt': 'Быстрая связь',
  'Wir sprechen Deutsch, Русский und Română': 'Говорим по-немецки, по-русски и по-румынски',
 },
 'ro': {
  'Stade · Buxtehude · Hamburg': 'Stade · Buxtehude · Hamburg',
  'Entrümpelung zum': 'Debarasare la',
  'Festpreis': 'preț fix',
  ', besenrein übergeben.': ', predat curat.',
  'Wohnungen, Häuser, Keller, Dachböden und Gewerbeflächen. Schicken Sie uns ein paar Fotos – Sie bekommen innerhalb von 24 Stunden ein verbindliches Angebot.': 'Apartamente, case, pivnițe, poduri și spații comerciale. Trimiteți-ne câteva fotografii – primiți o ofertă fermă în 24 de ore.',
  'Fotos per WhatsApp senden': 'Trimite poze pe WhatsApp',
  'Kosten schätzen': 'Estimează volumul',
  'Container für Restmüll': 'Container pentru gunoi',
  'Bei größeren Räumungen bestellen wir einen Container bei einem zugelassenen Entsorgungsfachbetrieb. Der Müll wird dort fachgerecht sortiert und verwertet – Sie haben keinen Aufwand.': 'La volume mari comandăm un container de la o firmă autorizată de gestionare a deșeurilor. Acolo gunoiul este sortat și reciclat corect — nu aveți nicio grijă.',
  '💬 Schreiben Sie uns per WhatsApp – unser Mitarbeiter ruft Sie zurück.': '💬 Scrieți-ne pe WhatsApp — un coleg vă sună înapoi.',
  'WhatsApp – wir rufen zurück': 'WhatsApp — vă sunăm noi',
  '🎥 Per Video schätzen': '🎥 Evaluare după video',
  'Genauer: Raum per Video scannen': 'Mai exact: evaluare după video',
  'Kostenlose Besichtigung vor Ort oder per Foto': 'Evaluare gratuită la fața locului sau după poze',
  'Festpreis ohne versteckte Kosten': 'Preț fix, fără costuri ascunse',
  'Fachgerechte Entsorgung und Recycling': 'Eliminare și reciclare conform legii',
  'Wertanrechnung für verwertbare Gegenstände': 'Scădem din preț valoarea obiectelor utilizabile',
  'Leistungen': 'Servicii',
  'Wir räumen, was Sie nicht mehr brauchen': 'Ridicăm tot ce nu vă mai trebuie',
  'Wohnungsentrümpelung': 'Debarasare apartamente',
  'Komplette Räumung von Mietwohnungen und Eigentum – auch kurzfristig vor der Wohnungsübergabe.': 'Golirea completă a apartamentelor închiriate sau proprietate – și urgent, înainte de predarea locuinței.',
  'Haushaltsauflösung': 'Lichidarea gospodăriei',
  'Nach Umzug ins Pflegeheim oder einem Todesfall. Ruhig, respektvoll, auf Wunsch ohne Ihre Anwesenheit.': 'După mutarea într-un cămin de bătrâni sau după un deces. Liniștit, cu respect, la cerere fără prezența dumneavoastră.',
  'Keller &amp; Dachboden': 'Pivniță și pod',
  'Schnell wieder Platz: Kellerabteile, Dachböden, Garagen und Gartenhäuser.': 'Faceți rapid loc: boxe, poduri, garaje și căsuțe de grădină.',
  'Messie-Wohnungen': 'Locuințe foarte aglomerate',
  'Diskrete Räumung stark vermüllter Wohnungen, mit Grundreinigung nach Absprache.': 'Golire discretă a locuințelor foarte încărcate, cu curățenie generală la cerere.',
  'Gewerbe &amp; Büro': 'Firme și birouri',
  'Büros, Lager und Ladenflächen – Möbel, Akten, Elektrogeräte, Regale.': 'Birouri, depozite și magazine – mobilier, dosare, aparate electrice, rafturi.',
  'Sperrmüll-Abholung': 'Ridicare deșeuri voluminoase',
  'Einzelne Möbel, Matratzen oder Elektrogeräte holen wir direkt bei Ihnen ab.': 'Ridicăm de la dumneavoastră mobilă, saltele sau aparate electrice.',
  'Ablauf': 'Cum lucrăm',
  "So einfach geht's": 'Foarte simplu',
  'Fotos oder Termin': 'Poze sau programare',
  'Fotos per WhatsApp schicken oder eine kostenlose Besichtigung vereinbaren.': 'Trimiteți poze pe WhatsApp sau programați o evaluare gratuită.',
  'Festpreis-Angebot': 'Ofertă cu preț fix',
  'Innerhalb von 24 Stunden erhalten Sie ein schriftliches Angebot.': 'În 24 de ore primiți o ofertă scrisă.',
  'Räumung': 'Golirea',
  'Wir kommen zum Wunschtermin, tragen alles raus und entsorgen fachgerecht.': 'Venim la data dorită, scoatem totul și eliminăm conform legii.',
  'Übergabe': 'Predarea',
  'Die Räume werden besenrein übergeben – bereit für Vermieter oder Käufer.': 'Spațiile sunt predate curate – gata pentru proprietar sau cumpărător.',
  'Preise': 'Prețuri',
  'Festpreis statt Stundenlohn': 'Preț fix, nu plată pe oră',
  'Besichtigung': 'Evaluare',
  'kostenlos': 'gratuit',
  'Angebot per Foto': 'Ofertă după poze',
  'in 24 Std.': 'în 24 de ore',
  'Arbeit, Transport, Entsorgung': 'Muncă, transport, eliminare',
  'im Festpreis': 'incluse în preț',
  'Wertanrechnung': 'Scăderea valorii obiectelor',
  'möglich': 'posibilă',
  'Versteckte Kosten': 'Costuri ascunse',
  'keine': 'niciunul',
  'Der Preis hängt von Menge, Etage und Zugang ab. Mit dem Rechner schätzen Sie die Menge – den verbindlichen Festpreis nennen wir Ihnen nach Fotos oder Besichtigung.': 'Prețul depinde de volum, etaj și acces. Cu calculatorul estimați volumul – prețul fix îl comunicăm după poze sau după evaluare.',
  'Objekt': 'Obiect',
  'Wohnung': 'Apartament',
  'Haus': 'Casă',
  'Keller / Dachboden': 'Pivniță / pod',
  'Gewerbe': 'Spațiu comercial',
  'Fläche (m²)': 'Suprafață (m²)',
  'Wie voll ist es?': 'Cât de plin este?',
  'Wenig': 'Puțin',
  'Normal': 'Normal',
  'Sehr voll': 'Foarte plin',
  'Etage ohne Aufzug': 'Etaj fără lift',
  'Erdgeschoss / mit Aufzug': 'Parter / cu lift',
  '1. Etage': 'Etajul 1',
  '2. Etage': 'Etajul 2',
  '3. Etage oder höher': 'Etajul 3 sau mai sus',
  'Geschätzte Menge Räumgut': 'Volum estimat de ridicat',
  'entspricht etwa 2 Transporterladungen · unverbindliche Schätzung': 'aproximativ 2 transporturi cu duba · estimare orientativă',
  'Festpreis per WhatsApp anfragen': 'Cere prețul pe WhatsApp',
  'Einsatzgebiet': 'Zona de lucru',
  'Stade, Hamburg und rund 100 km Umkreis': 'Stade, Hamburg și aproximativ 100 km în jur',
  'Häufige Fragen': 'Întrebări frecvente',
  'Gut zu wissen': 'Bine de știut',
  'Wie schnell können Sie räumen?': 'Cât de repede puteți goli?',
  'In der Regel innerhalb von 3–7 Tagen nach Auftrag, in dringenden Fällen auch kurzfristiger. Eine normale Wohnung räumen wir meist an einem Tag.': 'De obicei în 3–7 zile de la comandă, în cazuri urgente și mai repede. Un apartament obișnuit îl golim de regulă într-o zi.',
  'Muss ich bei der Räumung dabei sein?': 'Trebuie să fiu prezent?',
  'Nein. Sie können uns den Schlüssel übergeben. Nach der Räumung schicken wir Ihnen Fotos der leeren Räume.': 'Nu. Ne puteți lăsa cheia. După golire vă trimitem poze cu încăperile goale.',
  'Was passiert mit brauchbaren Möbeln?': 'Ce se întâmplă cu mobila bună?',
  'Verwertbare Gegenstände rechnen wir auf den Preis an oder geben sie an soziale Einrichtungen weiter. Der Rest wird getrennt und fachgerecht entsorgt.': 'Obiectele utilizabile le scădem din preț sau le donăm unor organizații sociale. Restul este sortat și eliminat conform legii.',
  'Ist der Preis wirklich fest?': 'Prețul este chiar fix?',
  'Ja. Nach der Besichtigung oder anhand Ihrer Fotos nennen wir einen Festpreis. Wenn nichts Unvorhergesehenes dazukommt, zahlen Sie genau diesen Betrag.': 'Da. După evaluare sau pe baza pozelor vă spunem un preț fix. Dacă nu apare nimic neprevăzut, plătiți exact această sumă.',
  'Wie bezahle ich?': 'Cum plătesc?',
  'Nach der Übergabe per Überweisung auf Rechnung. Für Privatkunden ist der Arbeitsanteil als haushaltsnahe Dienstleistung steuerlich absetzbar.': 'După predare, prin transfer bancar pe factură. Persoanele fizice pot deduce din impozit costul manoperei ca serviciu casnic (haushaltsnahe Dienstleistung).',
  'Jetzt kostenloses Angebot holen': 'Cereți acum o ofertă gratuită',
  'Schicken Sie 3–5 Fotos der Räume per WhatsApp. Wir melden uns noch am selben Tag mit einem Festpreis.': 'Trimiteți 3–5 poze cu încăperile pe WhatsApp. Vă răspundem în aceeași zi cu un preț fix.',
  'WhatsApp schreiben': 'Scrie pe WhatsApp',
  'Telefon / WhatsApp · Deutsch': 'Telefon / WhatsApp · în germană',
  'Erreichbar': 'Program',
  'Mo–Sa, 8–19 Uhr': 'Lun–Sâm, 8–19',
  '© 2026 Iltan Räumung · Entrümpelung in Stade &amp; Hamburg': '© 2026 Iltan Räumung · debarasări în Stade și Hamburg',
  'Anrufen': 'Sună',
  'Unsere Zusagen': 'Garanțiile noastre',
  'Kostenrechner': 'Calculator',
  'Schnellkontakt': 'Contact rapid',
  'Wir sprechen Deutsch, Русский und Română': 'Vorbim germană, rusă și română',
 },
}
JS = {
 'de': {'loads1':'entspricht etwa ','load':' Transporterladung','loads':' Transporterladungen','est':' · unverbindliche Schätzung','msg':'Hallo Iltan Räumung, ich möchte einen Festpreis anfragen: ','fill':', Füllgrad ','calc':'. Rechner-Schätzung: ','tail':' Räumgut. Fotos schicke ich gleich.','hero':'Hallo Iltan Räumung, ich möchte ein Angebot für eine Entrümpelung.','ca':'ca. ','f':{'leicht':'wenig','normal':'normal','voll':'sehr voll'}},
 'ru': {'loads1':'рейсов фургона: ~','load':'','loads':'','ca':'≈ ','est':' · предварительная оценка','msg':'Здравствуйте, Iltan Räumung! Хочу узнать фиксированную цену: ','fill':', заполненность: ','calc':'. Оценка калькулятора: ','tail':'. Фото пришлю сейчас.','hero':'Здравствуйте, Iltan Räumung! Хочу получить предложение на вывоз (пишу по-русски).','f':{'leicht':'немного','normal':'средне','voll':'очень много'}},
 'ro': {'loads1':'aproximativ ','load':' transport cu duba','loads':' transporturi cu duba','est':' · estimare orientativă','msg':'Bună ziua, Iltan Räumung! Aș dori un preț fix: ','fill':', grad de umplere: ','calc':'. Estimare calculator: ','tail':'. Trimit pozele imediat.','hero':'Bună ziua, Iltan Räumung! Aș dori o ofertă pentru debarasare (scriu în română).','ca':'cca. ','f':{'leicht':'puțin','normal':'normal','voll':'foarte plin'}},
}
META = {
 'de': ('Iltan Räumung','Entrümpelung, Haushaltsauflösung und Kellerräumung in Stade, Buxtehude und Hamburg. Kostenlose Besichtigung, Festpreis, besenreine Übergabe.'),
 'ru': ('Iltan Räumung — вывоз и освобождение помещений','Освобождение квартир, домов, подвалов и чердаков в Штаде, Букстехуде и Гамбурге. Бесплатный осмотр, фиксированная цена. Говорим по-русски.'),
 'ro': ('Iltan Räumung — debarasări','Debarasare apartamente, case, pivnițe și poduri în Stade, Buxtehude și Hamburg. Evaluare gratuită, preț fix. Vorbim românește.'),
}

def build(lang, src):
    s = src
    pre = '' if lang == 'de' else '../'
    # asset paths for subfolder pages
    if pre:
        for a in ('fonts/', 'icon-', 'manifest.webmanifest'):
            s = s.replace(f'"{a}', f'"{pre}{a}').replace(f'url({a}', f'url({pre}{a}')
        s = s.replace('<html lang="de">', f'<html lang="{lang}">')
        s = s.replace('href="https://iltan-raeumung.de/"', f'href="https://iltan-raeumung.de/{lang}/"')
        title, desc = META[lang]
        s = s.replace('<title>Iltan Räumung</title>', f'<title>{title}</title>')
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s)
        # translate visible text (only between tags / in aria-labels), longest first
        head, body = s.split('<body>', 1)
        legal_start = body.index('<div class="legal" id="impressum">')
        main, legal = body[:legal_start], body[legal_start:]
        foot = legal[legal.index('<footer>'):]
        legal = legal[:legal.index('<footer>')]
        H={'ru':'Освобождение помещений по <em>фиксированной цене</em>, сдаём чисто убранным.','ro':'Debarasare la <em>preț fix</em>, predat curat.'}[lang]
        main = main.replace('>Entrümpelung zum <em>Festpreis</em>, besenrein übergeben.<', '>'+H+'<')
        # RU/RO visitors get the Russian/Romanian-speaking number (contact list keeps both)
        m1, m2 = main.split('<div class="ph-de">', 1); keep, m3 = m2.split('</div>', 1)
        sw = lambda x: x.replace('4915111143537', '4917687800657').replace('0151 11143537', '0176 87800657')
        main = sw(m1) + '<div class="ph-de">' + keep + '</div>' + sw(m3)
        foot = sw(foot)
        main = main.replace('<label for="qm">Fläche (m²)', '<label for="qm">'+T[lang]['Fläche (m²)'])
        for de_txt in sorted(T[lang], key=len, reverse=True):
            tr = T[lang][de_txt]
            main = main.replace('>' + de_txt + '<', '>' + tr + '<').replace('aria-label="' + de_txt + '"', 'aria-label="' + tr + '"')
            foot = foot.replace('>' + de_txt + '<', '>' + tr + '<')
        note = {'ru': 'Юридическая информация приводится на немецком языке.', 'ro': 'Informațiile juridice sunt disponibile în limba germană.'}[lang]
        legal = legal.replace('<h2>Impressum</h2>', f'<h2>Impressum</h2>\n    <p><em>{note}</em></p>', 1)
        s = head + '<body>' + main + legal + foot
    # language switcher + languages line
    sw = '<nav class="langs" aria-label="Sprache">' + ''.join(
        f'<a href="{pre}{"" if l=="de" else l+"/"}" hreflang="{l}"{" aria-current=\"page\"" if l==lang else ""}>{l.upper()}</a>' for l in ('de','ru','ro')) + '</nav>'
    s = s.replace('<a class="tel"', sw + '\n      <a class="tel"', 1)
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="https://iltan-raeumung.de/{"" if l=="de" else l+"/"}">\n' for l in ('de','ru','ro'))
    s = s.replace('<link rel="canonical"', alt + '<link rel="canonical"', 1)
    langline = {'de':'Wir sprechen Deutsch, Русский und Română','ru':T['ru']['Wir sprechen Deutsch, Русский und Română'],'ro':T['ro']['Wir sprechen Deutsch, Русский und Română']}[lang]
    s = s.replace('<div><span>Erreichbar</span>', f'<div><span>Sprachen</span>{langline}</div>\n        <div><span>Erreichbar</span>', 1) if lang=='de' else s.replace(f'<div><span>{T[lang]["Erreichbar"]}</span>', f'<div><span>{ {"ru":"Языки","ro":"Limbi"}[lang] }</span>{langline}</div>\n        <div><span>{T[lang]["Erreichbar"]}</span>', 1)
    # JS strings
    j = JS[lang]
    s = s.replace("'entspricht etwa '+loads+' Transporterladung'+(loads>1?'en':'')+' · unverbindliche Schätzung'",
                  f"{json.dumps(j['loads1'])}+loads+(loads>1?{json.dumps(j['loads'])}:{json.dumps(j['load'])})+{json.dumps(j['est'])}")
    s = s.replace("var msg='Hallo Iltan Räumung, ich möchte einen Festpreis anfragen: '+objName+', ca. '+qm+' m², Füllgrad '+fill+', '+$('etage').selectedOptions[0].text+'. Rechner-Schätzung: '+$('price').textContent+' Räumgut. Fotos schicke ich gleich.';",
                  f"var FN={json.dumps(j['f'],ensure_ascii=False)};var msg={json.dumps(j['msg'],ensure_ascii=False)}+objName+', ~'+qm+' m²'+{json.dumps(j['fill'],ensure_ascii=False)}+FN[fill]+', '+$('etage').selectedOptions[0].text+{json.dumps(j['calc'],ensure_ascii=False)}+$('price').textContent+{json.dumps(j['tail'],ensure_ascii=False)};")
    hero_de = 'Hallo%20Iltan%20R%C3%A4umung%2C%20ich%20m%C3%B6chte%20ein%20Angebot%20f%C3%BCr%20eine%20Entr%C3%BCmpelung.'
    from urllib.parse import quote
    s = s.replace(hero_de, quote(j['hero']))
    if pre: s = s.replace('href="scan/"', f'href="../scan/?lang={lang}"')
    s = s.replace("$('price').textContent='ca. '+vol", "$('price').textContent="+json.dumps(j['ca'],ensure_ascii=False)+"+vol")
    s = s.replace("toLocaleString('de-DE')", f"toLocaleString('{ {'de':'de-DE','ru':'ru-RU','ro':'ro-RO'}[lang] }')")
    return s

CSS = """
.langs{display:flex;gap:4px;margin-left:auto}
.langs a{font:500 13px/1 var(--f-mono);letter-spacing:.06em;text-decoration:none;padding:7px 8px;border-radius:6px;opacity:.75}
.langs a[aria-current="page"]{background:var(--accent);color:var(--accent-ink);opacity:1}
.langs a:hover{opacity:1}
"""
if __name__ == '__main__':
    src = open('index.de.src.html').read() if os.path.exists('index.de.src.html') else open('index.html').read()
    if not os.path.exists('index.de.src.html'):
        open('index.de.src.html', 'w').write(src)
    src = src.replace('/* mobile action bar */', CSS + '/* mobile action bar */', 1)
    for lang in ('de', 'ru', 'ro'):
        out = 'index.html' if lang == 'de' else f'{lang}/index.html'
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        open(out, 'w').write(build(lang, src))
        print(out)
