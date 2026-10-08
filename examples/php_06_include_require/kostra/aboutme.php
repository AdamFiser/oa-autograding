<?php
// Výchozí stav: aplikace Maturita z cvičení PHP_02, stránka Profil.
// Všimněte si, kolik kódu má společného s index.php.

// --- ÚKOL 1: $authorName a APP_VERSION patří do includes/config.php ---
$authorName = 'yourName';
const APP_VERSION = '1.0';

$proposedTopic = 'Zabezpečení webových aplikací';
$status = 'čeká na schválení';

$supervisor = [
    'name' => 'Mgr. Jana Horáková',
    'email' => 'horakova@skola.cz',
    'room' => 'B204',
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
  <title>Profil | Maturita</title>

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
      <a href="index.php" class="text-gray-500 hover:text-brand-600">Přehled</a>
      <a href="aboutme.php" class="text-brand-600">Profil - <?php echo $authorName; ?></a>
    </div>
    <!-- ============ KONEC ČÁSTI PRO templates/menu.php ============ -->

  </nav>
</header>

<main class="flex-1 px-6 py-12">
  <div class="mx-auto max-w-3xl">
<!-- ============ KONEC ČÁSTI PRO templates/header.php ============ -->

    <div class="mb-8 rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
      <h1 class="mb-3 text-2xl font-semibold text-gray-800">Profil - <?php echo $authorName; ?></h1>
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

<!-- ============ ZAČÁTEK ČÁSTI PRO templates/footer.php (ÚKOL 4) ============ -->
  </div>
</main>

<footer class="border-t border-gray-200 bg-white py-4 text-center text-xs text-gray-400">
  Maturita v<?php echo APP_VERSION; ?>
</footer>

</body>
</html>
<!-- ============ KONEC ČÁSTI PRO templates/footer.php ============ -->
