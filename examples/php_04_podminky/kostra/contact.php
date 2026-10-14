<?php
$config = require __DIR__ . '/includes/config.php';

$pageTitle = 'Kontakt';
$activePage = 'contact';

include __DIR__ . '/templates/header.php';
?>

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Kontakt</h1>
      <p class="text-gray-500">
        Dotazy k maturitním pracím pište na
        <a href="mailto:<?php echo $config['email']; ?>" class="text-brand-600 hover:underline"><?php echo $config['email']; ?></a>
      </p>
    </div>

<?php include __DIR__ . '/templates/footer.php'; ?>
