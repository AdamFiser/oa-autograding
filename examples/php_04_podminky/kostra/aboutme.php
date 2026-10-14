<?php
// Výchozí stav: aplikace Maturita po cvičení PHP_06, stránka Profil.
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

// --- ÚKOL 4: stav tématu ---
// Stav se bere z adresy (aboutme.php?status=approved), jinak 'pending'.
// Možné hodnoty: 'approved', 'pending', 'rejected'.
$status = $_GET['status'] ?? 'pending';
$statusLabel = 'neznámý stav';
$statusClass = 'bg-gray-100 text-gray-600';

// --- ÚKOL 5: může odevzdat práci? ---
// Počet absolvovaných konzultací se bere z adresy (aboutme.php?consultations=3), jinak 2.
$myConsultations = (int) ($_GET['consultations'] ?? 2);
$requiredConsultations = 3;
$submitText = '';
$submitClass = 'text-gray-500';

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
      <p class="mt-2 font-medium <?php echo $submitClass; ?>"><?php echo $submitText; ?></p>
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
