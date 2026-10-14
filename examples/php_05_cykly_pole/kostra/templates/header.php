<!doctype html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="<?php echo $config['author']; ?>">
  <meta name="description" content="Maturita - portál pro správu maturitních prací">
  <title><?php echo $pageTitle; ?> | <?php echo $config['appName']; ?></title>

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
    <span class="text-lg font-semibold text-gray-800">📘 <?php echo $config['appName']; ?></span>

    <?php include __DIR__ . '/menu.php'; ?>

  </nav>
</header>

<main class="flex-1 px-6 py-12">
  <div class="mx-auto max-w-3xl">
