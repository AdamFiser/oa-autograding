<?php
declare(strict_types=1);
// Výchozí stav: aplikace Maturita po cvičení PHP_07, stránka Kontakt.
// Úkoly najdete v readme.md - značky ÚKOL ukazují, kam řešení patří.

// --- ÚKOL 6: session_start() ---

$config = require __DIR__ . '/includes/config.php';
// --- ÚKOL 1: načtěte knihovnu pro formuláře ---

$pageTitle = 'Kontakt';
$activePage = 'contact';

// Typy dotazu: hodnota ve formuláři => popis.
$typy = [
    'tema' => 'Výběr tématu',
    'konzultace' => 'Konzultace',
    'odevzdani' => 'Odevzdání práce',
];

// --- ÚKOL 4: po odeslání (POST) načtěte hodnoty a posbírejte chyby do $chyby ---
// --- ÚKOL 5: bez chyb přesměrujte na contact.php?odeslano=1 ---
// --- ÚKOL 6: odeslání s neplatným CSRF tokenem odmítněte kódem 403 ---

include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Kontakt</h1>
      <p class="text-gray-500">
        Dotazy k maturitním pracím pište na
        <a href="mailto:<?php echo $config['email']; ?>" class="text-brand-600 hover:underline"><?php echo $config['email']; ?></a>
        nebo přes formulář.
      </p>
    </div>

    <!-- ÚKOL 5: je-li v adrese odeslano, ukažte zprávu o přijetí dotazu -->

    <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-4 text-lg font-semibold text-gray-800">Napište vedoucímu práce</h3>
      <form action="contact.php" method="post" class="space-y-4 text-sm">
        <!-- ÚKOL 6: skryté pole s CSRF tokenem -->
        <div>
          <label for="jmeno" class="mb-1 block font-medium text-gray-700">Jméno</label>
          <input type="text" id="jmeno" name="jmeno" maxlength="50" class="w-full rounded-lg border border-gray-300 px-3 py-2">
          <!-- ÚKOL 4: vyplněná hodnota do value a chyba pole jmeno -->
        </div>
        <div>
          <label for="email" class="mb-1 block font-medium text-gray-700">E-mail</label>
          <input type="email" id="email" name="email" class="w-full rounded-lg border border-gray-300 px-3 py-2">
          <!-- ÚKOL 4: vyplněná hodnota do value a chyba pole email -->
        </div>
        <div>
          <label for="typ" class="mb-1 block font-medium text-gray-700">Typ dotazu</label>
          <select id="typ" name="typ" class="w-full rounded-lg border border-gray-300 px-3 py-2">
            <option value="">Vyberte…</option>
            <?php foreach ($typy as $hodnota => $popis) { ?>
              <option value="<?php echo $hodnota; ?>"><?php echo $popis; ?></option>
            <?php } ?>
          </select>
          <!-- ÚKOL 4: vybraný typ dostane selected, pod select chyba pole typ -->
        </div>
        <div>
          <label for="zprava" class="mb-1 block font-medium text-gray-700">Zpráva</label>
          <textarea id="zprava" name="zprava" rows="5" maxlength="1000" class="w-full rounded-lg border border-gray-300 px-3 py-2"></textarea>
          <!-- ÚKOL 4: vyplněný text mezi značky textarea a chyba pole zprava -->
        </div>
        <button type="submit" class="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white hover:bg-brand-700">Odeslat dotaz</button>
      </form>
    </div>

<?php include __DIR__ . '/templates/footer.php'; ?>
