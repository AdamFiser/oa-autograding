<?php
// Funkce aplikace Maturita. Soubor jen definuje funkce, nic nevypisuje.
// Úkoly najdete v readme.md - značky ÚKOL ukazují, kam řešení patří.

// --- ÚKOL 3: přepište tuto funkci ---
// Funguje, ale je napsaná špatně: data si bere přes `global`
// a výsledek rovnou vypisuje.
function printDeadline() {
    global $daysLeft, $daysCount, $daysWord;

    if ($daysLeft > 7) {
        $text = 'Do odevzdání zbývá ' . $daysLeft . ' ' . $daysWord . '.';
        $class = 'text-green-600';
    } elseif ($daysLeft > 0) {
        $text = 'Do odevzdání zbývá ' . $daysLeft . ' ' . $daysWord . '.';
        $class = 'text-amber-600';
    } elseif ($daysLeft === 0) {
        $text = 'Termín odevzdání je dnes!';
        $class = 'text-red-600';
    } else {
        $text = 'Termín odevzdání uplynul o ' . $daysCount . ' ' . $daysWord . '.';
        $class = 'text-red-600';
    }

    echo '<p class="mt-4 text-sm font-medium ' . $class . '">' . $text . '</p>';
}

// --- ÚKOL 2: getGreeting() a getDaysWord() ---


// --- ÚKOL 4: getGradeText() ---


// --- ÚKOL 5: calculateAverageGrade() ---


// --- ÚKOL 6: countConsultations() a findNextConsultation() ---


// --- ÚKOL 7: calculateWeeks() ---


// --- ÚKOL 8 (bonus): countChapters() ---
