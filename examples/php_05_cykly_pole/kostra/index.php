<?php
// Výchozí stav: aplikace Maturita po cvičení PHP_04, stránka Přehled.
// Úkoly najdete v README.md - značky ÚKOL ukazují, kam řešení patří.
$config = require __DIR__ . '/includes/config.php';

$pageTitle = 'Přehled';
$activePage = 'index';

$availableTopics = 24;
$myConsultations = 2;

// --- ÚKOL 2: tabulka historických témat ---
// Témat přibylo, ručně psané řádky tabulky už nestačí.
$topics = [
    ['title' => 'Rezervační systém pro autoškolu', 'author' => 'Jan Dvořák', 'year' => 2023, 'grade' => 1],
    ['title' => 'Webová galerie školních akcí', 'author' => 'Eva Malá', 'year' => 2024, 'grade' => 2],
    ['title' => 'Evidence výpůjček ve školní knihovně', 'author' => 'Petr Šťastný', 'year' => 2025, 'grade' => 1],
    ['title' => 'Online objednávky školní jídelny', 'author' => 'Lucie Krátká', 'year' => 2023, 'grade' => 3],
    ['title' => 'Kvízová aplikace pro výuku zeměpisu', 'author' => 'Tomáš Beneš', 'year' => 2024, 'grade' => 2],
    ['title' => 'Správa sportovního klubu', 'author' => 'Martin Kolář', 'year' => 2025, 'grade' => 4],
    ['title' => 'Plánovač školních rozvrhů', 'author' => 'Klára Veselá', 'year' => 2024, 'grade' => 1],
    ['title' => 'E-shop s výrobky studentské firmy', 'author' => 'David Novotný', 'year' => 2025, 'grade' => 4],
];

// --- ÚKOL 4: statistiky témat ---
$gradeSum = 0;
$bestGrade = 0;
$worstGrade = 0;
$averageGrade = 0;

// --- Pozdrav podle denní doby (z PHP_04) ---
// Hodina se bere z adresy stránky (index.php?hour=7). Když v adrese chybí,
// použije se aktuální hodina serveru (0-23).
$hour = (int) ($_GET['hour'] ?? date('G'));
if ($hour >= 22 || $hour < 5) {
    $greeting = 'Dobrou noc';
} elseif ($hour < 10) {
    $greeting = 'Dobré ráno';
} elseif ($hour < 18) {
    $greeting = 'Dobrý den';
} else {
    $greeting = 'Dobrý večer';
}

// --- Termín odevzdání (z PHP_04) ---
// Počet dní do odevzdání se bere z adresy (index.php?days=-3), jinak 12.
$daysLeft = (int) ($_GET['days'] ?? 12);
$daysCount = abs($daysLeft);
if ($daysCount === 1) {
    $daysWord = 'den';
} elseif ($daysCount >= 2 && $daysCount <= 4) {
    $daysWord = 'dny';
} else {
    $daysWord = 'dní';
}

if ($daysLeft > 7) {
    $deadlineText = 'Do odevzdání zbývá ' . $daysLeft . ' ' . $daysWord . '.';
    $deadlineClass = 'text-green-600';
} elseif ($daysLeft > 0) {
    $deadlineText = 'Do odevzdání zbývá ' . $daysLeft . ' ' . $daysWord . '.';
    $deadlineClass = 'text-amber-600';
} elseif ($daysLeft === 0) {
    $deadlineText = 'Termín odevzdání je dnes!';
    $deadlineClass = 'text-red-600';
} else {
    $deadlineText = 'Termín odevzdání uplynul o ' . $daysCount . ' ' . $daysWord . '.';
    $deadlineClass = 'text-red-600';
}

include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800"><?php echo $greeting; ?>, <?php echo $config['author']; ?>!</h1>
      <p class="text-gray-500">
        Maturita je portál, kde žáci procházejí historická maturitní
        témata, navrhují vlastní téma a sledují své konzultace s vedoucím
        práce.
      </p>
      <p class="mt-4 text-sm font-medium <?php echo $deadlineClass; ?>"><?php echo $deadlineText; ?></p>
    </div>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <?php
      // --- ÚKOL 4: karty vložte v cyklu ---
      $cardLabel = 'Dostupná témata';
      $cardValue = $availableTopics;
      include __DIR__ . '/templates/metric-card.php';

      $cardLabel = 'Moje konzultace';
      $cardValue = $myConsultations;
      include __DIR__ . '/templates/metric-card.php';
      ?>
    </div>

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
            <!-- ÚKOL 2 a 3: tři ručně psané řádky nahraďte cyklem foreach -->
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
