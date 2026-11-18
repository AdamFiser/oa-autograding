<?php
declare(strict_types=1);

// Knihovna pro formuláře. Soubor jen definuje funkce, nic nevypisuje a nic nevolá.
// Funkce dostávají data parametrem ($_GET, $_POST, $_FILES['foto']).

function nactiText(array $data, string $klic): string {
    $hodnota = $data[$klic] ?? '';

    if (!is_string($hodnota)) {        // útočník poslal pole: jmeno[]=x
        return '';
    }
    return trim($hodnota);
}

function escapuj(string $text): string {
    return htmlspecialchars($text);
}

function nactiVolbu(array $data, string $klic, array $povolene): ?string {
    $hodnota = $data[$klic] ?? null;
    return in_array($hodnota, $povolene, true) ? $hodnota : null;
}

function nactiCislo(array $data, string $klic, int $min, int $max): ?int {
    $cislo = filter_var($data[$klic] ?? null, FILTER_VALIDATE_INT, [
        'options' => ['min_range' => $min, 'max_range' => $max],
    ]);
    return $cislo === false ? null : $cislo;
}

function overText(string $text, string $nazev, int $maxDelka): ?string {
    if ($text === '') {
        return "Vyplňte pole $nazev.";
    }
    if (mb_strlen($text) > $maxDelka) {
        return "Pole $nazev může mít nejvýš $maxDelka znaků.";
    }
    return null;
}

function overEmail(string $email): ?string {
    if ($email === '') {
        return 'Vyplňte e-mail.';
    }
    if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
        return 'E-mail nemá správný formát.';
    }
    return null;
}

function presmeruj(string $adresa): never {
    header('Location: ' . $adresa, true, 303);
    exit;
}

function csrfToken(): string {
    $_SESSION['csrfToken'] ??= bin2hex(random_bytes(32));
    return $_SESSION['csrfToken'];
}

function overCsrfToken(array $data): bool {
    $token = $data['csrfToken'] ?? '';
    return is_string($token) && hash_equals(csrfToken(), $token);
}

function priponaObrazku(string $cesta): ?string {
    $povolene = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];
    $typ = mime_content_type($cesta);
    return $povolene[$typ] ?? null;
}

function overObrazek(?array $soubor, int $maxVelikost): ?string {
    if ($soubor === null || !is_int($soubor['error'] ?? null)) {
        return 'Vyberte jeden soubor.';
    }
    if ($soubor['error'] === UPLOAD_ERR_NO_FILE) {
        return 'Vyberte soubor.';
    }
    if ($soubor['error'] !== UPLOAD_ERR_OK) {
        return 'Soubor se nepodařilo nahrát.';
    }
    if ($soubor['size'] > $maxVelikost) {
        return 'Soubor je příliš velký.';
    }
    if (priponaObrazku($soubor['tmp_name']) === null) {
        return 'Povolené jsou jen obrázky JPG, PNG a WebP.';
    }
    return null;
}

function ulozObrazek(array $soubor, string $slozka): ?string {
    $nazev = bin2hex(random_bytes(16)) . '.' . priponaObrazku($soubor['tmp_name']);

    if (!move_uploaded_file($soubor['tmp_name'], $slozka . '/' . $nazev)) {
        return null;
    }
    return $nazev;
}

function nactiVolby(array $data, string $klic, array $povolene): array {
    $hodnoty = $data[$klic] ?? [];
    $vybrane = [];

    if (!is_array($hodnoty)) {
        return [];
    }
    foreach ($hodnoty as $hodnota) {
        if (in_array($hodnota, $povolene, true)) {
            $vybrane[] = $hodnota;
        }
    }
    return $vybrane;
}
