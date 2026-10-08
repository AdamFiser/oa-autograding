<div class="flex items-center gap-6 text-sm font-medium">
  <a href="index.php" class="<?php echo $activePage === 'index' ? 'text-brand-600' : 'text-gray-500 hover:text-brand-600'; ?>">Přehled</a>
  <a href="aboutme.php" class="<?php echo $activePage === 'aboutme' ? 'text-brand-600' : 'text-gray-500 hover:text-brand-600'; ?>">Profil - <?php echo $config['author']; ?></a>
  <a href="contact.php" class="<?php echo $activePage === 'contact' ? 'text-brand-600' : 'text-gray-500 hover:text-brand-600'; ?>">Kontakt</a>
</div>
