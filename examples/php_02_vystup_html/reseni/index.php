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
        <?php echo 'Hello, world!'; ?>
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

    <!-- ============ SEKCE JEN PRO index.php (ÚKOLY 7-12) ============

         V aboutme.php celou tuto sekci až po značku KONEC SEKCE smažte
         (viz ÚKOL 14). -->

    <div class="mt-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div class="border-b border-gray-100 px-5 py-4">
        <h3 class="text-lg font-semibold text-gray-800">Historická témata</h3>
      </div>

      <!-- --- ÚKOL 7 · index.php ---

           Do PHP bloku na začátku souboru deklarujte pole $topics se
           třemi historickými tématy. Každé téma je ASOCIATIVNÍ pole
           s klíči title, author, year a grade - celé $topics je tedy
           vícerozměrné pole. Použijte přesně tato data (další úkoly
           s nimi počítají):

             title                                  | author        | year | grade
             ---------------------------------------|---------------|------|------
             Rezervační systém pro autoškolu        | Jan Dvořák    | 2023 | 1
             Webová galerie školních akcí           | Eva Malá      | 2024 | 2
             Evidence výpůjček ve školní knihovně   | Petr Šťastný  | 2025 | 1

           Pozor na datové typy: year a grade jsou celá čísla (int),
           ne řetězce - pište je bez uvozovek.

           Pak nahraďte všechny pomlčky v tabulce níže hodnotami z pole
           pomocí echo, první buňka tedy vypíše $topics[0]['title'].
           Cyklus zatím neznáte, takže každou buňku vypíšete zvlášť.

           Očekávaný výstup: tabulka se třemi řádky podle dat výše,
           ve zdrojovém kódu stránky ani jedna pomlčka. -->
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="bg-gray-50 text-xs uppercase text-gray-500">
            <tr>
              <th class="px-5 py-3 font-medium">Název</th>
              <th class="px-5 py-3 font-medium">Autor</th>
              <th class="px-5 py-3 font-medium">Rok</th>
              <th class="px-5 py-3 font-medium">Známka</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr>
              <td class="px-5 py-3 font-medium text-gray-800"><?php echo $topics[0]['title']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[0]['author']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[0]['year']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[0]['grade']; ?></td>
            </tr>
            <tr>
              <td class="px-5 py-3 font-medium text-gray-800"><?php echo $topics[1]['title']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[1]['author']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[1]['year']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[1]['grade']; ?></td>
            </tr>
            <tr>
              <td class="px-5 py-3 font-medium text-gray-800"><?php echo $topics[2]['title']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[2]['author']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[2]['year']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topics[2]['grade']; ?></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="space-y-2 border-t border-gray-100 px-5 py-4 text-sm text-gray-500">

        <!-- --- ÚKOL 8 · index.php --- [+ odpověď v komentáři]

             Do odstavce níže vypište větu o nejnovějším tématu (poslední
             prvek pole $topics). Celou větu zapište JEDNÍM řetězcem
             v DVOJITÝCH UVOZOVKÁCH a hodnoty z pole do něj vložte
             přímo - bez tečky. U prvku vícerozměrného pole k tomu
             potřebujete složené závorky: "{$topics[2]['title']}".

             Očekávaný výstup:
             Nejnovější téma: Evidence výpůjček ve školní knihovně (2025, Petr Šťastný)

             Vyzkoušejte si stejný řetězec BEZ složených závorek a do
             komentáře napište, co PHP udělá.

             Odpověď:
        -->
        <p><?php echo "Nejnovější téma: {$topics[2]['title']} ({$topics[2]['year']}, {$topics[2]['author']})"; ?></p>

        <!-- --- ÚKOL 9 · index.php --- [+ odpověď v komentáři]

             Pracujte s názvem třetího tématu ($topics[2]['title'])
             a jménem jeho autora. Do tří odstavců níže vypište:

               a) počet znaků názvu funkcí mb_strlen() a v závorce
                  výsledek funkce strlen()
               b) název zkrácený na prvních 17 znaků funkcí mb_substr(),
                  za který připojíte tři tečky "..."
               c) jméno autora velkými písmeny funkcí mb_strtoupper()

             Očekávaný výstup:
             a) Délka názvu: 36 znaků (strlen: 42)
             b) Zkrácený název: Evidence výpůjček...
             c) Autor: PETR ŠŤASTNÝ

             Pak v b) zkuste substr() místo mb_substr() a v c)
             strtoupper() místo mb_strtoupper(). Do komentáře napište,
             co se na stránce pokazilo a proč strlen() vrací 42, když
             má název jen 36 znaků.

             Odpověď:
        -->
        <p><?php echo 'Délka názvu: ' . mb_strlen($topics[2]['title']) . ' znaků (strlen: ' . strlen($topics[2]['title']) . ')'; ?></p>
        <p>Zkrácený název: <?php echo mb_substr($topics[2]['title'], 0, 17) . '...'; ?></p>
        <p>Autor: <?php echo mb_strtoupper($topics[2]['author']); ?></p>

        <!-- --- ÚKOL 10 · index.php --- [+ odpověď v komentáři]

             Do PHP bloku na začátku souboru deklarujte proměnnou
             $averageGrade a přiřaďte do ní průměrnou známku všech tří
             témat - součet tří hodnot grade z pole $topics vydělený
             třemi. Nezapomeňte na závorky, násobení a dělení mají
             přednost před sčítáním.

             Průměr vypište do odstavce níže. Nejdřív přímo, pak
             zaokrouhlený na dvě desetinná místa funkcí
             round($averageGrade, 2) - na stránce nechte tu zaokrouhlenou.

             Očekávaný výstup:
             Průměrná známka: 1.33

             Do komentáře napište:
               - jaký datový typ má $averageGrade (ověřte var_dump())
               - jaký typ by měla, kdyby všechna tři témata měla
                 známku 1, a proč (vyzkoušejte, pak data vraťte zpět)

             Odpověď:
        -->
        <p>Průměrná známka: <?php echo round($averageGrade, 2); ?></p>
      </div>
    </div>

    <div class="mt-8 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-3 text-lg font-semibold text-gray-800">Hledání</h3>

      <!-- --- ÚKOL 11 · index.php --- [+ odpověď v komentáři]

           Stránka bude číst hledaný text z adresy - třeba
           http://localhost:8000/index.php?hledat=auto
           Formuláře přijdou až později, zatím parametr píšete do adresy
           ručně.

           Do PHP bloku na začátku souboru deklarujte:

             $searchQuery = trim($_GET['hledat'] ?? '');

           Operátor ?? vrátí prázdný řetězec, když parametr v adrese
           chybí, a trim() ořízne mezery na krajích.

           Do odstavců níže vypište:
             a) hledaný text uvnitř <strong> - obalený funkcí
                htmlspecialchars(), text přišel od uživatele
             b) jestli název PRVNÍHO tématu obsahuje hledaný text -
                výsledek funkce str_contains() přetypovaný na int, aby
                se místo prázdného místa vypsala 0

           Očekávaný výstup (zdrojový kód stránky):

             index.php?hledat=%20%20auto%20%20   (auto s mezerami okolo)
             Hledáte: <strong>auto</strong>
             Název prvního tématu obsahuje hledaný text: 1

             index.php?hledat=web
             Hledáte: <strong>web</strong>
             Název prvního tématu obsahuje hledaný text: 0

             index.php?hledat=<i>ahoj</i>
             Hledáte: <strong>&lt;i&gt;ahoj&lt;/i&gt;</strong>

           Do komentáře napište:
             - co se vypíše v b), když parametr hledat v adrese úplně
               chybí, a proč
             - co by se stalo s <i>ahoj</i> bez htmlspecialchars()

           Odpověď:
      -->
      <p class="text-sm text-gray-500">Hledáte: <strong><?php echo htmlspecialchars($searchQuery); ?></strong></p>
      <p class="text-sm text-gray-500">Název prvního tématu obsahuje hledaný text: <?php echo (int) str_contains($topics[0]['title'], $searchQuery); ?></p>
    </div>

    <div class="mt-8 rounded-2xl border border-dashed border-gray-300 bg-white p-5">
      <h3 class="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">Ladicí panel - datové typy</h3>

      <!-- --- ÚKOL 12 · index.php --- [+ odpověď v komentáři]

           Do PHP bloku na začátku souboru deklarujte ještě:

             $isRegistrationOpen = true;   // přihlašování témat běží
             $supervisorName = null;       // vedoucí zatím nepřidělen

           Do značky <pre> níže vypište funkcí var_dump() postupně:
           $availableTopics, $averageGrade, $topics[0]['title'],
           $isRegistrationOpen, $supervisorName a celé $topics[1].

           Do dvou odstavců pod panelem pak stejné dvě proměnné
           $isRegistrationOpen a $supervisorName vypište obyčejným
           výpisem pomocí echo.

           Očekávaný výstup (začátek panelu, čísla podle vašich hodnot):
             int(24)
             float(1.3333333333333333)
             string(35) "Rezervační systém pro autoškolu"
             bool(true)
             NULL
             array(4) { ...

           Do komentáře napište:
             - proč se u $topics[0]['title'] ukazuje string(35), když
               má název méně znaků (spojte s ÚKOLEM 9)
             - co vypsal obyčejný výpis true a null a proč se na ladění
               hodí var_dump()
             - co se stane, když značku <pre> smažete a proč

           Odpověď:
      -->
      <pre class="overflow-x-auto rounded-xl bg-gray-900 p-4 text-xs text-green-300">
<?php var_dump($availableTopics, $averageGrade, $topics[0]['title'], $isRegistrationOpen, $supervisorName, $topics[1]); ?>
      </pre>
      <p class="mt-3 text-sm text-gray-500">Přihlašování otevřeno: <?php echo $isRegistrationOpen; ?></p>
      <p class="text-sm text-gray-500">Vedoucí práce: <?php echo $supervisorName; ?></p>
    </div>

    <!-- ============ KONEC SEKCE JEN PRO index.php ============ -->

    

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
