<?php
$config = require __DIR__ . '/includes/config.php';

$pageTitle = 'Profil';
$activePage = 'aboutme';
// Výchozí stav: aplikace Maturita z cvičení PHP_02, stránka Profil.
// Všimněte si, kolik kódu má společného s index.php.


$proposedTopic = 'Zabezpečení webových aplikací';
$status = 'čeká na schválení';

$supervisor = [
    'name' => 'Mgr. Jana Horáková',
    'email' => 'horakova@skola.cz',
    'room' => 'B204',
];
include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Profil - <?php echo $config['author']; ?></h1>
      <p class="text-gray-500">Navržené téma: <?php echo $proposedTopic; ?></p>
      <p class="text-sm text-gray-400">Stav: <?php echo $status; ?></p>
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
