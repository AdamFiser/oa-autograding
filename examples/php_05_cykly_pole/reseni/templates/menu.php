<div class="flex items-center gap-6 text-sm font-medium">
  <?php foreach ($config['menu'] as $page => $label) { ?>
    <a href="<?php echo $page; ?>.php" class="<?php echo $activePage === $page ? 'text-brand-600' : 'text-gray-500 hover:text-brand-600'; ?>"><?php echo $label; ?></a>
  <?php } ?>
</div>
