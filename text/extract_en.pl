#!/usr/bin/perl -w
# takes a lines in groups of 3: 1 ja, 1 en, 1 blank.
# outputs the en line, with any quote marks or metachars from the ja line.
use Encode;
use File::Slurp;

for(read_file("names.txt")) {
    $_ = decode("utf8", $_, Encode::FB_CROAK);
    chomp;
    /^(\S+) (\S+)$/ or die;
    $name{$1} = $2;
}

$state = 'blank or ja';
while(<>) {
    $_ = decode("utf8", $_, Encode::FB_CROAK);
    s/\s*$//;
    m#^ *//# and next;
    if(/^(%[NOPp])+$/ or /^(%FS)?-{40,}[%A-Z0-9]+$/) {
        print "$_\n";
        $state = 'blank or ja';
    } elsif($state eq 'blank or ja' and /^$/) {
    } elsif($state =~ 'ja') {
        $p = $_;
        $state = 'en';
        if(s/\x{2473}/  /g) { # "It's an infinity loop"
            print encode("shift_jis", "$_\n", Encode::FB_CROAK);
            $state = 'blank or ja';
        }
    } elsif($state eq 'en') {
        s/\s*((?:%[KNOP])+)$//; # override the original escape codes if the translation specifies some
        my $en_linebreak = $1;
        s/%(?![A-Z])/\x{ff05}/g; # % is a metachar, but the lookalike char isn't
        s/\x{ff5e}/\x{301c}/g; # two versions of tilde, only one of which has a shift_jis codepoint
        s/\x{2013}|\x{2014}/\x{2015}/g; # likewise for mdash '―'
		s/\x{2015}\x{2015}/\x{2015}/g; # double -> single emdash
        # s/\x{ff0d}/__WMINUS__/g; # fullwidth minus hyphen
        s/\x{ff0d}/-/g; # fullwidth minus hyphen -> '-'
        ($en_linebreak || $p) =~ /%K$/ and $_ .= " "; # no trailing newline, so the sentence will be continued
        s/(?<!\b\S \S)  +/ /g; # collapse multiple spaces unless there are also extra spaces within the neighboring words
        #s/ /  /g; # spaces are too thin on pc; Not the case for psp.
        #$p =~ s/%TS\d+|%TE//g; # remove tips. any that make sense will be in the translation.
        s/''(I)''/%CFF8F$1%CFFFF/g; # colored text (yellow) to signify "ore", as deviated from Kokoro's normal "watashi".
        s/'(I)'/%C8CFF$1%CFFFF/g; # colored text (blue) to signify "watashi", as deviated from Satoru's normal "ore".
        s/\x{014d}/o/g; # 'ō'. no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
        s/na\x{ef}ve/naive/g; # no umlaut for i
        s/\x{00e9}/e/g; # é (utf8:c3a9) in fiancé; SA5_07
        # s/\x{2473}/__U2473__/g; # ⑳ ('CIRCLED NUMBER TWENTY' (U+2473)). Is rendered as a wide space. (glyph #1147)
        /''/ and die "unmatched ''";
        $meta = "(?:%[A-Zp][A-Z0-9]*)*";
        $p =~ /^($meta)((?:.*?\x{300c})?).*?((?:\x{300d}.*)?$meta)$/;
        my $line = $1;
        my $speaker = $2;
        my $trailing = $3;
        if($speaker) {
            $speaker =~ s/\x{300c}$//;
            $line .= join ", ", map {$name{$_} || $_} split /\x{30fb}/, $speaker;
            $line .= "\x{300c}";
        }
        if($_ =~ /"/ and $speaker eq "" and $trailing =~ s/\x{300d}[\x{3000}-\x{ffff}]+//) {
            # for one line in CO4_02.txt with text after the end-quote
            $line = "";
        }
        $line .= "$_$trailing\n";
        if($en_linebreak) {
            $line =~ s/(%[KNOP])+\n//;
            $line .= $en_linebreak . "\n";
        }

        # check for buffer overflow. the game will probably run out of space on screen
        # before this, but that's harder to check given a variable width font.
        $page .= $line;
        if($line =~ /%[PO]/) {
            $page =~ s/\n|%[KNOP]|%C....|%TS...|%TE//g;
            # Standard psp engine limit is 480
            my $MAX_PAGE = 480;
            if(length($page) > $MAX_PAGE) {
                warn "too much text on one page (".length($page)." > $MAX_PAGE chars) at $ARGV line $.\n";
            }
            $page = "";
        }

        # print encode("shift_jis", $line, Encode::FB_CROAK);
        $_ = encode("shift_jis", $line, Encode::FB_CROAK);
		# Manual replacement
        # s/__U2473__/\x{87}\x{53}/g;
        # s/__WMINUS__/\x{81}\x{7c}/g;
		print;
        $state = 'blank';
    } elsif($state eq 'blank') {
        /\S/ and die "$0 desync at \"$ARGV\" line $.\n";
        $state = 'blank or ja';
    }
}
