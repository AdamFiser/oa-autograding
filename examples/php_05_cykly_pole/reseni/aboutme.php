<?php
// Výchozí stav: aplikace Maturita po cvičení PHP_04, stránka Profil.
// Úkoly najdete v README.md - značky ÚKOL ukazují, kam řešení patří.
$config = require __DIR__ . '/includes/config.php';

$pageTitle = 'Profil';
$activePage = 'aboutme';

$proposedTopic = 'Zabezpečení webových aplikací';

$supervisor = [
    'name' => 'Mgr. Jana Horáková',
    'email' => 'horakova@skola.cz',
    'room' => 'B204',
];

// --- Stav tématu (z PHP_04) ---
// Stav se bere z adresy (aboutme.php?status=approved), jinak 'pending'.
$status = $_GET['status'] ?? 'pending';

$statusLabel = match ($status) {
    'approved' => 'schváleno',
    'pending' => 'čeká na schválení',
    'rejected' => 'zamítnuto',
    default => 'neznámý stav',
};
$statusClass = match ($status) {
    'approved' => 'bg-green-100 text-green-700',
    'pending' => 'bg-amber-100 text-amber-700',
    'rejected' => 'bg-red-100 text-red-700',
    default => 'bg-gray-100 text-gray-600',
};

// --- ÚKOL 5: konzultace ---
// Stav konzultace: 'done' = absolvovaná, 'planned' = naplánovaná, 'cancelled' = zrušená.
$consultations = [
    ['date' => '24. 9. 2026', 'topic' => 'Výběr tématu', 'state' => 'done'],
    ['date' => '8. 10. 2026', 'topic' => 'Osnova práce', 'state' => 'done'],
    ['date' => '22. 10. 2026', 'topic' => 'Analýza zadání', 'state' => 'cancelled'],
    ['date' => '5. 11. 2026', 'topic' => 'Návrh databáze', 'state' => 'planned'],
    ['date' => '19. 11. 2026', 'topic' => 'Prototyp aplikace', 'state' => 'planned'],
];
$myConsultations = 0;
$nextConsultation = 'žádná není naplánovaná';
$requiredConsultations = 3;

foreach ($consultations as $consultation) {
    if ($consultation['state'] === 'done') {
        $myConsultations++;
    }
}

foreach ($consultations as $consultation) {
    if ($consultation['state'] === 'planned') {
        $nextConsultation = $consultation['date'] . ' – ' . $consultation['topic'];
        break;
    }
}

// --- Může odevzdat práci? (z PHP_04) ---
$hasEnoughConsultations = $myConsultations >= $requiredConsultations;
$isTopicApproved = $status === 'approved';

if ($hasEnoughConsultations && $isTopicApproved) {
    $submitText = 'Můžete odevzdat maturitní práci.';
    $submitClass = 'text-green-600';
} elseif (!$isTopicApproved) {
    $submitText = 'Nejdříve musí být schválené téma.';
    $submitClass = 'text-red-600';
} else {
    $submitText = 'Chybí ještě ' . ($requiredConsultations - $myConsultations) . ' konzultace.';
    $submitClass = 'text-amber-600';
}

// --- ÚKOL 7 (bonus): plán psaní ---
$pagesTotal = 30;
$pagesPerWeek = 4;
$weeksNeeded = 0;

$pagesWritten = 0;
while ($pagesWritten < $pagesTotal) {
    $pagesWritten += $pagesPerWeek;
    $weeksNeeded++;
}

include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Profil - <?php echo $config['author']; ?></h1>
      <p class="text-gray-500">Navržené téma: <?php echo $proposedTopic; ?></p>
      <p class="mt-3 text-sm text-gray-400">
        Stav: <span class="rounded-full px-3 py-1 text-xs font-medium <?php echo $statusClass; ?>"><?php echo $statusLabel; ?></span>
      </p>
    </div>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-3 text-lg font-semibold text-gray-800">Odevzdání práce</h3>
      <p class="text-sm text-gray-500">Konzultace: <?php echo $myConsultations; ?> z <?php echo $requiredConsultations; ?></p>
      <div class="mt-3 flex gap-2">
        <?php for ($i = 1; $i <= $requiredConsultations; $i++) {
          $stepClass = $i <= $myConsultations ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-400';
        ?>
          <span class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium <?php echo $stepClass; ?>"><?php echo $i; ?></span>
        <?php } ?>
      </div>
      <p class="mt-2 font-medium <?php echo $submitClass; ?>"><?php echo $submitText; ?></p>
      <p class="mt-2 text-sm text-gray-500">Při <?php echo $pagesPerWeek; ?> stranách týdně napíšete <?php echo $pagesTotal; ?> stran za <?php echo $weeksNeeded; ?> týdnů.</p>
    </div>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-3 text-lg font-semibold text-gray-800">Konzultace</h3>
      <ul class="space-y-2 text-sm text-gray-600">
        <?php foreach ($consultations as $consultation) {
          if ($consultation['state'] === 'cancelled') {
              continue;
          }
          $stateLabel = $consultation['state'] === 'done' ? 'absolvována' : 'naplánována';
        ?>
          <li><?php echo $consultation['date']; ?> – <?php echo $consultation['topic']; ?> (<?php echo $stateLabel; ?>)</li>
        <?php } ?>
      </ul>
      <p class="mt-4 text-sm text-gray-500">Nejbližší konzultace: <?php echo $nextConsultation; ?></p>
    </div>

    <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
      <h3 class="mb-3 text-lg font-semibold text-gray-800">Vedoucí práce</h3>
      <p class="font-medium text-gray-800"><?php echo $supervisor['name']; ?></p>
      <p class="text-sm text-gray-500">
        E-mail: <a href="mailto:<?php echo $supervisor['email']; ?>" class="text-brand-600 hover:underline"><?php echo $supervisor['email']; ?></a>
      </p>
      <p class="text-sm text-gray-500">Kabinet: <?php echo $supervisor['room']; ?></p>
    </div>

<?php include __DIR__ . '/templates/footer.php'; ?>
