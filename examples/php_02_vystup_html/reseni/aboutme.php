<?php
const APP_VERSION = "1.0";
$authorName = 'Karel Novak';
$availableTopics = 24;
$myConsultations = 2;
$topics = [
    ['title' => 'Rezervační systém pro autoškolu', 'author' => 'Jan Dvořák', 'year' => 2023, 'grade' => 1],
    ['title' => 'Webová galerie školních akcí', 'author' => 'Eva Malá', 'year' => 2024, 'grade' => 2],
    ['title' => 'Evidence výpůjček ve školní knihovně', 'author' => 'Petr Šťastný', 'year' => 2025, 'grade' => 1],
];
$averageGrade = ($topics[0]['grade'] + $topics[1]['grade'] + $topics[2]['grade']) / 3;
$searchQuery = trim($_GET['hledat'] ?? '');
$isRegistrationOpen = true;
$supervisorName = null;
$proposedTopic = 'Zabezpeceni webovych aplikaci';
$consultationDate = '2026-10-02';
$status = 'ceka na schvaleni';
const REQUIRED_CONSULTATIONS = 3;
$consultationProgress = (int) ($myConsultations / REQUIRED_CONSULTATIONS * 100);
$supervisor = [
    'name' => 'Mgr. Jana Horáková',
    'email' => 'horakova@skola.cz',
    'room' => 'B204',
];
$supervisorPhone = $supervisor['phone'] ?? 'neuvedeno';
$messageTemplate = "Dobry den, {jmeno},\nvase tema {tema} bylo prijato k posouzeni.\nS pozdravem, {vedouci}";
?>
<!-- ============ JAK POSTUPOVAT ============

     Úkoly jsou očíslované přesně v pořadí, ve kterém je děláte.
     Každý má u čísla štítek souboru, ve kterém ho řešíte.

       FÁZE A - ÚKOLY 1-13  (index.php)
         Postupujte souborem odshora dolů, čísla jdou po sobě.
         Úkoly označené "FÁZE B" zatím přeskočte.

       FÁZE B - ÚKOL 14      vytvoří kopii aboutme.php (úplně dole v souboru)
                ÚKOLY 15-20  (aboutme.php, ÚKOL 15 i v index.php)
         Začínají znovu nahoře v souboru - hledejte je podle čísla.

     Přehled všech úkolů v jedné tabulce najdete v README.md.

     --- ÚKOL 1 · index.php ---

     Na úplný začátek souboru (nad tento komentář i nad `<!doctype html>`)
     vložte PHP blok `<?php /* deklarace */ ?>` a deklarujte v něm tři
     proměnné:

       $authorName        - vaše jméno
       $availableTopics   - kolik historických témat je v aplikaci k dispozici (číslo, např. 24)
       $myConsultations   - kolik konzultací jste už měli (číslo, např. 2)

     Do tohoto bloku budete i v dalších úkolech přidávat proměnné,
     pole a konstanty - co přesně deklarovat, najdete vždy u zadání
     daného úkolu, ale píšete to sem, na začátek souboru. -->
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- --- ÚKOL 2 · index.php ---

       Tenhle blok <head> zatím obsahuje statický text. Nahraďte VŠECHNY
       textové uzly (obsah <title> a atribut content u meta tagu
       description níže) výstupem PHP - použijte echo nebo print.

       Očekávaný výstup: v prohlížeči (Ctrl+U, zobrazit zdrojový kód)
       vidíte stejný text jako teď - jen ho tam nedostal statický HTML,
       ale echo/print.

       --- ÚKOL 3 · index.php ---

       Atribut content u meta tagu author níže nahraďte hodnotou
       proměnné $authorName (ÚKOL 1) - do uvozovek atributu content
       vložte PHP blok, který proměnnou vypíše pomocí echo.

       Očekávaný výstup (zdrojový kód stránky): meta name="author"
       content="Karel Novak" (s vaším jménem místo yourName) -->
  <meta name="author" content="<?php echo $authorName; ?>">
  <meta name="description" content="<?php echo 'Maturita - portal pro spravu maturitnich prací'; ?>">
  <title><?php echo 'Maturita'; ?></title>

  <!-- Tailwind CSS přes Play CDN - žádný build krok, jen script tag.
       Paleta barev brand-* je definovaná v konfiguraci níže. -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          fontFamily: { outfit: ["Outfit", "sans-serif"] },
          colors: {
            brand: {
              25: "#f2f7ff", 50: "#ecf3ff", 100: "#dde9ff", 500: "#465fff",
              600: "#3641f5", 700: "#2a31d8"
            }
          }
        }
      }
    };
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>

<body class="flex min-h-screen flex-col bg-gray-50 font-outfit text-gray-800">

<header class="border-b border-gray-200 bg-white">
  <nav class="mx-auto flex max-w-3xl items-center justify-between px-6 py-4">
    <span class="text-lg font-semibold text-gray-800">📘 Maturita</span>

    <!-- --- ÚKOL 4 · index.php ---

         Text odkazu "Profil" níže nahraďte textem "Profil - <vaše_jméno>",
         kde <vaše_jméno> je HODNOTA proměnné $authorName (ÚKOL 1) - jméno
         tedy do textu nepište přímo, spojte ho s textem "Profil - " pomocí
         tečky (.) nebo v uvozovkách přes $authorName.

         Očekávaný výstup (zdrojový kód stránky): Profil - Karel Novak
         (s vaším jménem, stejná hodnota jako v meta author z ÚKOLU 3)

         --- ÚKOL 15 · index.php i aboutme.php (FÁZE B) ---

         Oba odkazy níže mají zatím placeholder href="#" - nikam nevedou.
         V OBOU souborech je upravte tak, aby fungovaly obousměrně:
         odkaz Přehled ať vede na `index.php` a odkaz Profil na
         `aboutme.php` - v obou souborech stejně. -->
    <div class="flex items-center gap-6 text-sm font-medium">
      <a href="index.php" class="text-brand-600">Přehled</a>
      <a href="aboutme.php" class="text-gray-500 hover:text-brand-600"><?php echo 'Profil - ' . $authorName; ?></a>
    </div>
  </nav>
</header>

<main class="flex-1 px-6 py-12">
  <div class="mx-auto max-w-3xl">

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">

      <!-- --- ÚKOL 5 · index.php ---

           Do uvítacího nadpisu H1 vložte PHP kód, který vypíše text
           `Hello, world!`, a výstup vyzkoušejte v prohlížeči.

           Očekávaný výstup: Hello, world!

           --- ÚKOL 16 · aboutme.php (FÁZE B) ---

           Na kopii (aboutme.php) přepište stejný nadpis H1 na
           "Profil - <vaše_jméno>" - stejně jako v ÚKOLU 4, tedy
           "Profil - " spojené s hodnotou $authorName. Na index.php
           zůstává Hello, world!. -->
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">
        <?php echo 'Profil - ' . $authorName; ?>
      </h1>
      <p class="text-gray-500">
        Maturita je portál, kde žáci procházejí historická maturitní
        témata, navrhují vlastní téma a sledují své konzultace s vedoucím
        práce.
      </p>
    </div>

    <!-- Metrikové karty. Zatím se statickými čísly, hodnoty doplníte
         v ÚKOLU 6. -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50">
          <svg class="fill-brand-600" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M8.80443 5.60156C7.59109 5.60156 6.60749 6.58517 6.60749 7.79851C6.60749 9.01185 7.59109 9.99545 8.80443 9.99545C10.0178 9.99545 11.0014 9.01185 11.0014 7.79851C11.0014 6.58517 10.0178 5.60156 8.80443 5.60156ZM5.10749 7.79851C5.10749 5.75674 6.76267 4.10156 8.80443 4.10156C10.8462 4.10156 12.5014 5.75674 12.5014 7.79851C12.5014 9.84027 10.8462 11.4955 8.80443 11.4955C6.76267 11.4955 5.10749 9.84027 5.10749 7.79851ZM4.86252 15.3208C4.08769 16.0881 3.70377 17.0608 3.51705 17.8611C3.48384 18.0034 3.5211 18.1175 3.60712 18.2112C3.70161 18.3141 3.86659 18.3987 4.07591 18.3987H13.4249C13.6343 18.3987 13.7992 18.3141 13.8937 18.2112C13.9797 18.1175 14.017 18.0034 13.9838 17.8611C13.7971 17.0608 13.4132 16.0881 12.6383 15.3208C11.8821 14.572 10.6899 13.955 8.75042 13.955C6.81096 13.955 5.61877 14.572 4.86252 15.3208ZM3.8071 14.2549C4.87163 13.2009 6.45602 12.455 8.75042 12.455C11.0448 12.455 12.6292 13.2009 13.6937 14.2549C14.7397 15.2906 15.2207 16.5607 15.4446 17.5202C15.7658 18.8971 14.6071 19.8987 13.4249 19.8987H4.07591C2.89369 19.8987 1.73504 18.8971 2.05628 17.5202C2.28015 16.5607 2.76117 15.2906 3.8071 14.2549Z" fill=""/>
          </svg>
        </div>
        <div class="mt-4">
          <span class="text-sm text-gray-500">Dostupná témata</span>

          <!-- --- ÚKOL 6 · index.php ---

               Nahraďte statické číslo níže hodnotou proměnné
               $availableTopics (ÚKOL 1) pomocí echo.

               Očekávaný výstup: číslo, které jste přiřadili $availableTopics. -->
          <h4 class="mt-1 text-2xl font-bold text-gray-800"><?php echo $availableTopics; ?></h4>
        </div>
      </div>

      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50">
          <svg class="stroke-brand-600" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 7V3M16 7V3M4 11H20M6 5H18C19.1046 5 20 5.89543 20 7V19C20 20.1046 19.1046 21 18 21H6C4.89543 21 4 20.1046 4 19V7C4 5.89543 4.89543 5 6 5Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="mt-4">
          <span class="text-sm text-gray-500">Moje konzultace</span>

          <!-- --- ÚKOL 6 (pokračování) ---

               Nahraďte statické číslo níže hodnotou proměnné
               $myConsultations (ÚKOL 1) pomocí echo.

               Očekávaný výstup: číslo, které jste přiřadili $myConsultations. -->
          <h4 class="mt-1 text-2xl font-bold text-gray-800"><?php echo $myConsultations; ?></h4>
        </div>
      </div>
    </div>

    

    <!-- ============ FÁZE B · SEKCE JEN PRO aboutme.php (ÚKOLY 17-20) ============

         Ve FÁZI A (index.php) tuto sekci přeskočte - úkoly v ní patří
         až na stránku aboutme.php, která vznikne v ÚKOLU 14.
         V index.php pak celou sekci až po značku KONEC SEKCE smažte
         (viz ÚKOL 14). -->

    <!-- --- ÚKOL 17 · aboutme.php ---

         Do PHP bloku na začátku aboutme.php přidejte proměnné
         $proposedTopic (název vašeho navrženého tématu),
         $consultationDate (datum poslední konzultace) a $status (stav
         návrhu, např. "ceka na schvaleni").

         Pak přímo sem, pod tento komentář, přidejte novou <section>
         a do ní vypište všechny tři proměnné na jednom řádku přesně
         v tomto formátu, aby šel výstup zkontrolovat:

         Tema: <hodnota $proposedTopic> | Konzultace: <hodnota $consultationDate> | Stav: <hodnota $status>

         Očekávaný výstup (příklad):
         Tema: Zabezpeceni webovych aplikaci | Konzultace: 2026-10-02 | Stav: ceka na schvaleni -->
    <section class="mt-8 text-sm text-gray-500">
      <?php echo "Tema: $proposedTopic | Konzultace: $consultationDate | Stav: $status"; ?>
    </section>

    <div class="mt-8 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

      <!-- --- ÚKOL 18 · aboutme.php --- [+ odpověď v komentáři]

           Do PHP bloku na začátku souboru (vedle APP_VERSION z ÚKOLU 13)
           deklarujte konstantu

             const REQUIRED_CONSULTATIONS = 3;

           a proměnnou $consultationProgress - kolik procent povinných
           konzultací máte za sebou: $myConsultations vydělené
           REQUIRED_CONSULTATIONS a vynásobené 100, celé přetypované
           na (int).

           Pak ve výpisu níže nahraďte:
             - text "0 z 0 (0 %)" hodnotami $myConsultations,
               REQUIRED_CONSULTATIONS a $consultationProgress
             - hodnotu 0 v atributu style="width: 0%" proměnnou
               $consultationProgress - PHP tak přímo řídí šířku
               ukazatele na stránce

           Očekávaný výstup (zdrojový kód stránky, pro $myConsultations = 2):
             2 z 3 (66 %)
             style="width: 66%"

           Do komentáře napište:
             - co vypíše var_dump() výpočtu BEZ přetypování na (int)
             - proč vyšlo 66 a ne 67

           Odpověď:
      -->
      <div class="mb-2 flex items-center justify-between text-sm">
        <span class="font-medium text-gray-800">Postup konzultací</span>
        <span class="text-gray-500"><?php echo $myConsultations . ' z ' . REQUIRED_CONSULTATIONS . ' (' . $consultationProgress . ' %)'; ?></span>
      </div>
      <div class="h-2.5 w-full rounded-full bg-gray-100">
        <div class="h-2.5 rounded-full bg-brand-500" style="width: <?php echo $consultationProgress; ?>%"></div>
      </div>
    </div>

    <!-- --- ÚKOL 19 · aboutme.php --- [+ odpověď v komentáři]

         Do PHP bloku na začátku souboru deklarujte asociativní pole
         s údaji o vedoucím práce:

           $supervisor = [
               'name' => 'Mgr. Jana Horáková',
               'email' => 'horakova@skola.cz',
               'room' => 'B204',
           ];

         a proměnnou $supervisorPhone, do které operátorem ?? uložíte
         $supervisor['phone'], nebo text "neuvedeno", když klíč phone
         v poli chybí (a on chybí).

         Statickou kartu níže přepište tak, že CELOU vypíšete jedním
         příkazem echo s víceřádkovým textem - heredocem (<<<HTML ...
         HTML;). Hodnoty z pole do něj vložte se složenými závorkami
         jako v ÚKOLU 8, včetně adresy v atributu href.

         Očekávaný výstup (zdrojový kód stránky, mimo jiné):
           <a href="mailto:horakova@skola.cz" ...>horakova@skola.cz</a>
           Telefon: neuvedeno

         Do komentáře napište, co PHP vypíše, když místo
         $supervisorPhone dáte do heredocu rovnou {$supervisor['phone']}.

         Odpověď:
    -->
<?php
echo <<<HTML
    <div class="mt-8 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-3 text-lg font-semibold text-gray-800">Vedoucí práce</h3>
      <p class="font-medium text-gray-800">{$supervisor['name']}</p>
      <p class="text-sm text-gray-500">
        E-mail: <a href="mailto:{$supervisor['email']}" class="text-brand-600 hover:underline">{$supervisor['email']}</a>
      </p>
      <p class="text-sm text-gray-500">Kabinet: {$supervisor['room']}</p>
      <p class="text-sm text-gray-500">Telefon: $supervisorPhone</p>
    </div>

HTML;
?>

    <!-- --- ÚKOL 20 · aboutme.php --- [bonus + odpověď v komentáři]

         Aplikace posílá žákům zprávy podle předem připravené šablony.
         Do PHP bloku na začátku souboru deklarujte šablonu - POZOR,
         v dvojitých uvozovkách, jinak se \n nepřevede na nový řádek:

           $messageTemplate = "Dobry den, {jmeno},\nvase tema {tema} bylo prijato k posouzeni.\nS pozdravem, {vedouci}";

         Funkcí str_replace() postupně nahraďte zástupné texty {jmeno},
         {tema} a {vedouci} hodnotami $authorName, $proposedTopic
         a $supervisor['name']. Nakonec ještě jedním str_replace()
         nahraďte "\n" značkou <br> a hotovou zprávu vypište do
         <blockquote> níže.

         Očekávaný výstup (zdrojový kód stránky, s vašimi hodnotami):
         Dobry den, Karel Novak,<br>vase tema Zabezpeceni webovych aplikaci bylo prijato k posouzeni.<br>S pozdravem, Mgr. Jana Horáková

         Do komentáře napište, jak zpráva vypadala v prohlížeči, dokud
         jste \n nenahradili za <br>, a proč.

         Odpověď:
    -->
    <blockquote class="mt-8 rounded-2xl border-l-4 border-brand-500 bg-brand-25 p-5 text-sm text-gray-700">
      <?php
      $message = str_replace('{jmeno}', $authorName, $messageTemplate);
      $message = str_replace('{tema}', $proposedTopic, $message);
      $message = str_replace('{vedouci}', $supervisor['name'], $message);
      echo str_replace("\n", '<br>', $message);
      ?>
    </blockquote>

    <!-- ============ KONEC SEKCE JEN PRO aboutme.php ============ -->

  </div>
</main>

<footer class="border-t border-gray-200 bg-white py-4 text-center text-xs text-gray-400">

  <!-- --- ÚKOL 13 · index.php ---

       Deklarujte konstantu `const APP_VERSION = "1.0";` (v PHP bloku na
       začátku souboru, spolu s proměnnými) a verzi zobrazte v patičce
       pomocí této konstanty (bez `$` - konstanty se na rozdíl od
       proměnných vypisují přímo jménem, bez `$`). Kopie v ÚKOLU 14
       patičku převezme, na aboutme.php ji už psát nemusíte.

       Očekávaný výstup: Maturita v1.0 -->
  Maturita v<?php echo APP_VERSION; ?>
</footer>

<!-- --- ÚKOL 14 · vytvoření aboutme.php (začátek FÁZE B) ---

     Tady končí FÁZE A. Než budete pokračovat, zkontrolujte, že má
     index.php hotové ÚKOLY 1-13.

     Pak:
       1. Zkopírujte index.php a kopii uložte jako aboutme.php.
       2. V aboutme.php smažte SEKCI JEN PRO index.php (ÚKOLY 7-12).
       3. V index.php smažte SEKCI JEN PRO aboutme.php (ÚKOLY 17-20).

     Pokračujte ÚKOLEM 15 - najdete ho nahoře v navigaci. -->

</body>
</html>
