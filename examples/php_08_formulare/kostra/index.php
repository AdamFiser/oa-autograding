<?php
declare(strict_types=1);
// Výchozí stav: aplikace Maturita po cvičení PHP_07, stránka Přehled.
// Úkoly najdete v readme.md - značky ÚKOL ukazují, kam řešení patří.

$config = require __DIR__ . '/includes/config.php';
require_once __DIR__ . '/includes/functions.php';
// --- ÚKOL 1: načtěte i knihovnu pro formuláře ---

$pageTitle = 'Přehled';
$activePage = 'index';

$availableTopics = 24;
$myConsultations = 2;

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

$bestGrade = $topics[0]['grade'];
$worstGrade = $topics[0]['grade'];
foreach ($topics as $topic) {
    if ($topic['grade'] < $bestGrade) {
        $bestGrade = $topic['grade'];
    }
    if ($topic['grade'] > $worstGrade) {
        $worstGrade = $topic['grade'];
    }
}
$averageGrade = calculateAverageGrade($topics);

// --- ÚKOL 3: načtěte hledaný text a rok z formuláře, témata vyfiltrujte funkcí filterTopics() ---

// --- ÚKOL 2: hodnoty z adresy čtěte přes nactiCislo() ---
// Hodina se bere z adresy stránky (index.php?hour=7). Když v adrese chybí,
// použije se aktuální hodina serveru (0-23).
$hour = (int) ($_GET['hour'] ?? date('G'));
$greeting = getGreeting($hour);

// Počet dní do odevzdání se bere z adresy (index.php?days=-3), jinak 12.
$daysLeft = (int) ($_GET['days'] ?? 12);

include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800"><?php echo $greeting; ?>, <?php echo $config['author']; ?>!</h1>
      <p class="text-gray-500">
        Maturita je portál, kde žáci procházejí historická maturitní
        témata, navrhují vlastní téma a sledují své konzultace s vedoucím
        práce.
      </p>
      <p class="mt-4 text-sm font-medium <?php echo getDeadlineClass($daysLeft); ?>"><?php echo getDeadlineText($daysLeft); ?></p>
    </div>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <?php
      $cards = [
          ['label' => 'Dostupná témata', 'value' => $availableTopics],
          ['label' => 'Moje konzultace', 'value' => $myConsultations],
          ['label' => 'Průměrná známka', 'value' => $averageGrade],
          ['label' => 'Nejlepší / nejhorší známka', 'value' => $bestGrade . ' / ' . $worstGrade],
      ];

      foreach ($cards as $card) {
          $cardLabel = $card['label'];
          $cardValue = $card['value'];
          include __DIR__ . '/templates/metric-card.php';
      }
      ?>
    </div>

    <div class="mt-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
      <div class="border-b border-gray-100 px-5 py-4">
        <h3 class="text-lg font-semibold text-gray-800">Historická témata</h3>
        <!-- ÚKOL 3: formulář si pamatuje zadání - value u pole hledat, selected u vybraného roku -->
        <form action="index.php" method="get" class="mt-3 flex flex-wrap items-center gap-2 text-sm">
          <input type="search" name="hledat" maxlength="50" placeholder="Hledat v názvu…" class="min-w-0 flex-1 rounded-lg border border-gray-300 px-3 py-2">
          <select name="rok" class="rounded-lg border border-gray-300 px-3 py-2">
            <option value="">Všechny roky</option>
            <option value="2023">2023</option>
            <option value="2024">2024</option>
            <option value="2025">2025</option>
          </select>
          <!-- ÚKOL 8 (bonus): checkboxy znamka[] s hodnotami 1 až 5 -->
          <button type="submit" class="rounded-lg bg-brand-600 px-4 py-2 font-medium text-white hover:bg-brand-700">Hledat</button>
        </form>
        <!-- ÚKOL 3: počet nalezených témat a hledaný text -->
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
            <!-- ÚKOL 3: vypisujte jen nalezená témata -->
            <?php foreach ($topics as $index => $topic) {
              $rowClass = $index % 2 === 1 ? 'bg-gray-50' : 'bg-white';
            ?>
            <tr class="<?php echo $rowClass; ?>">
              <td class="px-5 py-3 font-medium text-gray-800"><?php echo $topic['title']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topic['author']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topic['year']; ?></td>
              <td class="px-5 py-3 text-gray-500"><?php echo $topic['grade']; ?> (<?php echo getGradeText($topic['grade']); ?>)</td>
            </tr>
            <?php } ?>
          </tbody>
        </table>
      </div>
    </div>

<?php include __DIR__ . '/templates/footer.php'; ?>
