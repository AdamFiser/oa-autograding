<?php
declare(strict_types=1);

session_start();

$config = require __DIR__ . '/includes/config.php';
require_once __DIR__ . '/includes/formular.php';

$pageTitle = 'Kontakt';
$activePage = 'contact';

// Typy dotazu: hodnota ve formuláři => popis.
$typy = [
    'tema' => 'Výběr tématu',
    'konzultace' => 'Konzultace',
    'odevzdani' => 'Odevzdání práce',
];

$chyby = [];
$jmeno = nactiText($_POST, 'jmeno');
$email = nactiText($_POST, 'email');
$typ = nactiVolbu($_POST, 'typ', array_keys($typy));
$zprava = nactiText($_POST, 'zprava');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!overCsrfToken($_POST)) {
        http_response_code(403);
        exit('Neplatný token. Načtěte stránku a odešlete formulář znovu.');
    }

    $chyby = array_filter([
        'jmeno' => overText($jmeno, 'jméno', 50),
        'email' => overEmail($email),
        'typ' => $typ === null ? 'Vyberte typ dotazu.' : null,
        'zprava' => overText($zprava, 'zpráva', 1000),
    ]);

    if ($chyby === []) {
        presmeruj('contact.php?odeslano=1');
    }
}

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

    <?php if (isset($_GET['odeslano'])) { ?>
      <p class="mb-8 rounded-2xl border border-green-200 bg-green-50 p-5 text-center font-medium text-green-700">Děkujeme, dotaz jsme přijali.</p>
    <?php } ?>

    <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-4 text-lg font-semibold text-gray-800">Napište vedoucímu práce</h3>
      <form action="contact.php" method="post" class="space-y-4 text-sm">
        <input type="hidden" name="csrfToken" value="<?php echo csrfToken(); ?>">
        <div>
          <label for="jmeno" class="mb-1 block font-medium text-gray-700">Jméno</label>
          <input type="text" id="jmeno" name="jmeno" maxlength="50" value="<?php echo escapuj($jmeno); ?>" class="w-full rounded-lg border border-gray-300 px-3 py-2">
          <p class="mt-1 text-red-600"><?php echo escapuj($chyby['jmeno'] ?? ''); ?></p>
        </div>
        <div>
          <label for="email" class="mb-1 block font-medium text-gray-700">E-mail</label>
          <input type="email" id="email" name="email" value="<?php echo escapuj($email); ?>" class="w-full rounded-lg border border-gray-300 px-3 py-2">
          <p class="mt-1 text-red-600"><?php echo escapuj($chyby['email'] ?? ''); ?></p>
        </div>
        <div>
          <label for="typ" class="mb-1 block font-medium text-gray-700">Typ dotazu</label>
          <select id="typ" name="typ" class="w-full rounded-lg border border-gray-300 px-3 py-2">
            <option value="">Vyberte…</option>
            <?php foreach ($typy as $hodnota => $popis) { ?>
              <option value="<?php echo $hodnota; ?>"<?php echo $typ === $hodnota ? ' selected' : ''; ?>><?php echo $popis; ?></option>
            <?php } ?>
          </select>
          <p class="mt-1 text-red-600"><?php echo escapuj($chyby['typ'] ?? ''); ?></p>
        </div>
        <div>
          <label for="zprava" class="mb-1 block font-medium text-gray-700">Zpráva</label>
          <textarea id="zprava" name="zprava" rows="5" maxlength="1000" class="w-full rounded-lg border border-gray-300 px-3 py-2"><?php echo escapuj($zprava); ?></textarea>
          <p class="mt-1 text-red-600"><?php echo escapuj($chyby['zprava'] ?? ''); ?></p>
        </div>
        <button type="submit" class="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white hover:bg-brand-700">Odeslat dotaz</button>
      </form>
    </div>

<?php include __DIR__ . '/templates/footer.php'; ?>
