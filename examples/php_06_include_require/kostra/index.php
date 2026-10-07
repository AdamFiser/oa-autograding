<?php
// Výchozí stav: aplikace Maturita z cvičení PHP_02, stránka Přehled.
// Úkoly najdete v README.md - tady jsou jen značky, které ukazují,
// kterou část kódu v kterém úkolu přesouváte.

// --- ÚKOL 1: $authorName a APP_VERSION patří do includes/config.php ---
$authorName = 'yourName';
const APP_VERSION = '1.0';

$availableTopics = 24;
$myConsultations = 2;

$topics = [
    ['title' => 'Rezervační systém pro autoškolu', 'author' => 'Jan Dvořák', 'year' => 2023, 'grade' => 1],
    ['title' => 'Webová galerie školních akcí', 'author' => 'Eva Malá', 'year' => 2024, 'grade' => 2],
    ['title' => 'Evidence výpůjček ve školní knihovně', 'author' => 'Petr Šťastný', 'year' => 2025, 'grade' => 1],
];
?>
<!-- ============ ZAČÁTEK ČÁSTI PRO templates/header.php (ÚKOL 2) ============ -->
<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="<?php echo $authorName; ?>">
  <meta name="description" content="Maturita - portál pro správu maturitních prací">
  <title>Přehled | Maturita</title>

  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
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

    <!-- ============ ZAČÁTEK ČÁSTI PRO templates/menu.php (ÚKOL 3) ============ -->
    <div class="flex items-center gap-6 text-sm font-medium">
      <a href="index.php" class="text-brand-600">Přehled</a>
      <a href="aboutme.php" class="text-gray-500 hover:text-brand-600">Profil - <?php echo $authorName; ?></a>
    </div>
    <!-- ============ KONEC ČÁSTI PRO templates/menu.php ============ -->

  </nav>
</header>

<main class="flex-1 px-6 py-12">
  <div class="mx-auto max-w-3xl">
<!-- ============ KONEC ČÁSTI PRO templates/header.php ============ -->

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Vítejte, <?php echo $authorName; ?>!</h1>
      <p class="text-gray-500">
        Maturita je portál, kde žáci procházejí historická maturitní
        témata, navrhují vlastní téma a sledují své konzultace s vedoucím
        práce.
      </p>
    </div>

    <!-- ============ METRIKOVÉ KARTY (ÚKOL 6) ============
         Obě karty jsou až na popisek a číslo stejné. -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-xl">📊</div>
        <div class="mt-4">
          <span class="text-sm text-gray-500">Dostupná témata</span>
          <h4 class="mt-1 text-2xl font-bold text-gray-800"><?php echo $availableTopics; ?></h4>
        </div>
      </div>

      <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-xl">📊</div>
        <div class="mt-4">
          <span class="text-sm text-gray-500">Moje konzultace</span>
          <h4 class="mt-1 text-2xl font-bold text-gray-800"><?php echo $myConsultations; ?></h4>
        </div>
      </div>
    </div>
    <!-- ============ KONEC METRIKOVÝCH KARET ============ -->

    <div class="mt-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div class="border-b border-gray-100 px-5 py-4">
        <h3 class="text-lg font-semibold text-gray-800">Historická témata</h3>
      </div>
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
    </div>

<!-- ============ ZAČÁTEK ČÁSTI PRO templates/footer.php (ÚKOL 4) ============ -->
  </div>
</main>

<footer class="border-t border-gray-200 bg-white py-4 text-center text-xs text-gray-400">
  Maturita v<?php echo APP_VERSION; ?>
</footer>

</body>
</html>
<!-- ============ KONEC ČÁSTI PRO templates/footer.php ============ -->
