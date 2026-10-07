<?php
$config = require __DIR__ . '/includes/config.php';

$pageTitle = 'Přehled';
$activePage = 'index';
// Výchozí stav: aplikace Maturita z cvičení PHP_02, stránka Přehled.
// Úkoly najdete v README.md - tady jsou jen značky, které ukazují,
// kterou část kódu v kterém úkolu přesouváte.


$availableTopics = 24;
$myConsultations = 2;

$topics = [
    ['title' => 'Rezervační systém pro autoškolu', 'author' => 'Jan Dvořák', 'year' => 2023, 'grade' => 1],
    ['title' => 'Webová galerie školních akcí', 'author' => 'Eva Malá', 'year' => 2024, 'grade' => 2],
    ['title' => 'Evidence výpůjček ve školní knihovně', 'author' => 'Petr Šťastný', 'year' => 2025, 'grade' => 1],
];
include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Vítejte, <?php echo $config['author']; ?>!</h1>
      <p class="text-gray-500">
        Maturita je portál, kde žáci procházejí historická maturitní
        témata, navrhují vlastní téma a sledují své konzultace s vedoucím
        práce.
      </p>
    </div>

    <!-- ============ METRIKOVÉ KARTY (ÚKOL 6) ============
         Obě karty jsou až na popisek a číslo stejné. -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <?php
      $cardLabel = 'Dostupná témata';
      $cardValue = $availableTopics;
      include __DIR__ . '/templates/metric-card.php';

      $cardLabel = 'Moje konzultace';
      $cardValue = $myConsultations;
      include __DIR__ . '/templates/metric-card.php';
      ?>
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

<?php include __DIR__ . '/templates/footer.php'; ?>
