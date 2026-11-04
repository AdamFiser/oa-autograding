<?php
declare(strict_types=1);

// Funkce aplikace Maturita. Soubor jen definuje funkce, nic nevypisuje.

function getGreeting(int $hour): string {
    if ($hour >= 22 || $hour < 5) {
        return 'Dobrou noc';
    }
    if ($hour < 10) {
        return 'Dobré ráno';
    }
    if ($hour < 18) {
        return 'Dobrý den';
    }

    return 'Dobrý večer';
}

function getDaysWord(int $days): string {
    $count = abs($days);
    if ($count === 1) {
        return 'den';
    }
    if ($count >= 2 && $count <= 4) {
        return 'dny';
    }

    return 'dní';
}

function getDeadlineText(int $daysLeft): string {
    if ($daysLeft > 0) {
        return 'Do odevzdání zbývá ' . $daysLeft . ' ' . getDaysWord($daysLeft) . '.';
    }
    if ($daysLeft === 0) {
        return 'Termín odevzdání je dnes!';
    }

    return 'Termín odevzdání uplynul o ' . abs($daysLeft) . ' ' . getDaysWord($daysLeft) . '.';
}

function getDeadlineClass(int $daysLeft): string {
    if ($daysLeft > 7) {
        return 'text-green-600';
    }
    if ($daysLeft > 0) {
        return 'text-amber-600';
    }

    return 'text-red-600';
}

function getGradeText(int $grade): string {
    return match ($grade) {
        1 => 'výborně',
        2 => 'chvalitebně',
        3 => 'dobře',
        4 => 'dostatečně',
        5 => 'nedostatečně',
        default => 'neznámá známka',
    };
}

function calculateAverageGrade(array $topics): float {
    if (count($topics) === 0) {
        return 0.0;
    }

    $gradeSum = 0;
    foreach ($topics as $topic) {
        $gradeSum += $topic['grade'];
    }

    return round($gradeSum / count($topics), 2);
}

function countConsultations(array $consultations, string $state = 'done'): int {
    $count = 0;
    foreach ($consultations as $consultation) {
        if ($consultation['state'] === $state) {
            $count++;
        }
    }

    return $count;
}

function findNextConsultation(array $consultations): ?string {
    foreach ($consultations as $consultation) {
        if ($consultation['state'] === 'planned') {
            return $consultation['date'] . ' – ' . $consultation['topic'];
        }
    }

    return null;
}

function calculateWeeks(int $pagesTotal, int $pagesPerWeek): int {
    $pagesWritten = 0;
    $weeks = 0;
    while ($pagesWritten < $pagesTotal) {
        $pagesWritten += $pagesPerWeek;
        $weeks++;
    }

    return $weeks;
}

function countChapters(array $chapters): int {
    $count = 0;
    foreach ($chapters as $chapter) {
        $count += 1 + countChapters($chapter['chapters']);
    }

    return $count;
}
