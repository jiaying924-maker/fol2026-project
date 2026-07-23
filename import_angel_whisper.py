#!/usr/bin/env python3
"""
Angel's Whisper CSV Importer for FOL 2026
Imports messages from CSV directly to Firebase
"""

import csv
import sys
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Participant list (matching profile page)
PARTICIPANTS = [
    {'name': 'DR. FONG', 'full': 'FONG TOH JENG', 'outlet': 'HQ'},
    {'name': 'DR. JAYE', 'full': 'TAN SOO HUA', 'outlet': 'HQ'},
    {'name': 'DR. JOVYN', 'full': 'NG CHIA WEN', 'outlet': 'HQ'},
    {'name': 'DR NICOLE', 'full': 'NICOLE NG I', 'outlet': 'HQ'},
    {'name': 'DR XUAN', 'full': 'LIM WEN XUAN', 'outlet': 'HQ'},
    {'name': 'DR JEM', 'full': 'LIM JIA YING', 'outlet': 'HQ'},
    {'name': 'YU CHUEN', 'full': 'YU CHUEN', 'outlet': 'HQ'},
    {'name': 'JIA XUAN', 'full': 'LIM JIA XUAN', 'outlet': 'HQ'},
    {'name': 'CHING THING', 'full': 'KOAY CHING THING', 'outlet': 'HQ'},
    {'name': 'KHAI XUAN', 'full': 'TAN KHAI XUAN', 'outlet': 'HQ'},
    {'name': 'CELINE', 'full': 'CELINE TEH SHYEH YIN', 'outlet': 'HQ'},
    {'name': 'CAROL', 'full': 'TAN EE ING', 'outlet': 'HQ'},
    {'name': 'LIANG', 'full': 'HONG CHOO LIANG', 'outlet': 'HQ'},
    {'name': 'XIN RU', 'full': 'YEOH XIN RU', 'outlet': 'HQ'},
    {'name': 'CATHERINE', 'full': 'LAO HONG HONG', 'outlet': 'HQ'},
    {'name': 'JINNY', 'full': 'LIM JING YEE', 'outlet': 'HQ'},
    {'name': 'SHUE HUI', 'full': 'KOAY SHUE HUI', 'outlet': 'HQ'},
    {'name': 'TK', 'full': 'NG TIEN KHOON', 'outlet': 'HQ'},
    {'name': 'ADELINE', 'full': 'LEE KHE HUONG', 'outlet': 'HQ'},
    {'name': '叶老师', 'full': 'YEAP WENG HOE', 'outlet': 'HQ'},
    {'name': 'NICOLE', 'full': 'YEE WEI TING', 'outlet': 'PG'},
    {'name': 'PHEI CHIA', 'full': 'CHEE TOO PHEI CHIA', 'outlet': 'PG'},
    {'name': 'WENNIE', 'full': 'NEOW WENNIE', 'outlet': 'BM'},
    {'name': 'ESTHER', 'full': 'LOW KER YEE', 'outlet': 'BM'},
    {'name': 'HONEY', 'full': 'HONEY CHONG THEAN MI', 'outlet': 'BM'},
    {'name': 'SHERLYN', 'full': 'TAN YING SING', 'outlet': 'BM'},
    {'name': 'WAN YING', 'full': 'NGO WAN YING', 'outlet': 'BM'},
    {'name': 'ENNA', 'full': 'LAW YI ERN', 'outlet': 'BM'},
    {'name': 'TIFFANY', 'full': 'NG SHI HUI', 'outlet': 'BM'},
    {'name': 'VENUS', 'full': 'TEE YEE SYUEN', 'outlet': 'BM'},
    {'name': 'YEN SI', 'full': 'TAN YEN SI', 'outlet': 'BM'},
    {'name': 'AI MEI', 'full': 'CHAN AI MEI', 'outlet': 'BM'},
    {'name': 'YE YING', 'full': 'TAN YE YING', 'outlet': 'BM'},
    {'name': 'YVONNE', 'full': 'ANG YVONNE', 'outlet': 'BM'},
    {'name': 'ELAINE', 'full': 'TAN JIA SHYUAN', 'outlet': 'BM'},
    {'name': 'JANICE', 'full': 'KHOR YI TING', 'outlet': 'BM'},
    {'name': 'DR HONG', 'full': 'HONG JIA JUN', 'outlet': 'BM'},
    {'name': 'DR LEENA', 'full': 'LIM LEE NAA', 'outlet': 'BM'},
    {'name': 'DR JOLING', 'full': 'CHEW PHOAY KOON', 'outlet': 'BM'},
    {'name': 'DR EE LING', 'full': 'TAN EE LING', 'outlet': 'BM'},
    {'name': 'DR.JOYCE', 'full': 'JOYCE ONG ZIZHI', 'outlet': 'GL'},
    {'name': 'MINDY', 'full': 'CHEW SEE MENG', 'outlet': 'GL'},
    {'name': 'SYVIN', 'full': 'FOO LI SHAN', 'outlet': 'GL'},
    {'name': 'HUI XIAN', 'full': 'KHOO HUI XIAN', 'outlet': 'GL'},
    {'name': 'JANICE', 'full': 'KHOO WEI SIN', 'outlet': 'GL'},
    {'name': 'STELLA', 'full': 'TAN CHI YAN', 'outlet': 'GL'},
    {'name': 'KATHERINE', 'full': 'CHAI XIN JIE', 'outlet': 'GL'},
    {'name': 'YUNNY', 'full': 'ANG YUN QI', 'outlet': 'GL'},
    {'name': 'KARENE', 'full': 'HON YI TING', 'outlet': 'GL'},
    {'name': 'REGINA', 'full': "REGINA CH'NG PEI XUAN", 'outlet': 'GL'},
    {'name': 'XIAO WEI', 'full': "CH'NG XIAO WEI", 'outlet': 'GL'},
    {'name': 'YEN HOON', 'full': 'OON YEN HOON', 'outlet': 'GL'},
    {'name': 'CHLOE', 'full': 'LEE WAN YU', 'outlet': 'GL'},
    {'name': 'IRIS', 'full': 'OOI TZE YEE', 'outlet': 'GL'},
    {'name': 'TIFFANY', 'full': 'CHENG ZHI EN', 'outlet': 'GL'},
    {'name': 'ESTHER', 'full': 'ESTHER TAN JIA YING', 'outlet': 'GL'},
    {'name': 'DR CHERYL', 'full': 'CHERYL LOW YEE WEN', 'outlet': 'GL'},
    {'name': 'DR MICHELLE', 'full': 'MICHELLE KOK WAN YING', 'outlet': 'GL'},
    {'name': 'DR CHAN', 'full': 'CHAN SZE YUET', 'outlet': 'GL'},
    {'name': 'DR YI WEN', 'full': 'TAN YI WEN', 'outlet': 'GL'},
    {'name': 'CLARISE', 'full': 'CHUAH JING PING', 'outlet': 'GY'},
    {'name': 'MARGARET', 'full': 'MARGARET CHIN SIEW THENG', 'outlet': 'GY'},
    {'name': 'IRIS', 'full': 'IRIS LUAH JIE YING', 'outlet': 'GY'},
    {'name': 'AVICIA', 'full': 'CHENG ZHI YI', 'outlet': 'GY'},
    {'name': 'QUNNIE', 'full': 'GOH YU QIAN', 'outlet': 'GY'},
    {'name': 'MANDY', 'full': 'MANDY NG ZHI CHING', 'outlet': 'GY'},
    {'name': 'DR EVE', 'full': 'YUEN SHAN LING', 'outlet': 'GY'},
    {'name': 'DR SHEVERN', 'full': 'SHEVERN YEOH YU RUUN', 'outlet': 'GY'},
    {'name': 'YY', 'full': 'LIM YEE YIN', 'outlet': 'RU'},
    {'name': 'YEE JING', 'full': 'CHAI YEE JING', 'outlet': 'RU'},
    {'name': 'YAYA', 'full': 'CHIEW ZIN HUA', 'outlet': 'RU'},
    {'name': 'KE XIN', 'full': 'TAN KE XIN', 'outlet': 'RU'},
    {'name': 'JANET', 'full': 'JANET YUN JING HUI', 'outlet': 'RU'},
    {'name': 'SAFENIE', 'full': 'UN MIN QIN', 'outlet': 'RU'},
    {'name': 'YEE ANN', 'full': 'CHUA YEE ANN', 'outlet': 'RU'},
    {'name': 'YI LING', 'full': 'TAN YI LING', 'outlet': 'RU'},
    {'name': 'DR LOO', 'full': 'LOO SHI JIN', 'outlet': 'RU'},
    {'name': 'DR ROZANNE', 'full': 'CHANG HUI XIAN', 'outlet': 'RU'},
    {'name': 'DR.KAI', 'full': 'HONG KHYE HUNG', 'outlet': 'RU'},
    {'name': 'SHARON', 'full': 'NG SAN FOO', 'outlet': 'JB'},
    {'name': 'BEIER', 'full': 'KHOR BEI SI', 'outlet': 'MA'},
    {'name': 'XUE JING', 'full': 'TAN SIOK CHING', 'outlet': 'MA'},
    {'name': 'JASYE', 'full': 'LEE JIA YI', 'outlet': 'MA'},
    {'name': 'PEI SHIN', 'full': 'LEW PEI SHIN', 'outlet': 'MA'},
    {'name': 'JIA LIN', 'full': 'LEY JIA LIN', 'outlet': 'MA'},
    {'name': 'DR JJ', 'full': 'LEE JIA JING', 'outlet': 'MA'},
    {'name': 'DR KENNY', 'full': 'ANG YEE QUAN', 'outlet': 'MA'},
    {'name': 'DR LILY', 'full': 'TANG SZE LI', 'outlet': 'MA'},
    {'name': 'RAYNA', 'full': 'RAYNA LIM', 'outlet': 'MA'},
    {'name': 'JESSY', 'full': 'FANG HUI YEN', 'outlet': 'MA'},
    {'name': 'BERYL', 'full': 'BERYL LIM SEOK HWEE', 'outlet': 'MA'},
    {'name': 'THING THING', 'full': 'CHEW THING THING', 'outlet': 'MA'},
    {'name': 'XIANG YEE', 'full': 'KHOO XIANG YEE', 'outlet': 'MA'},
    {'name': 'XIIAO CHYN', 'full': 'XIIAO CHYN', 'outlet': 'MA'},
    {'name': 'SANNY', 'full': 'SONG KE', 'outlet': 'SU'},
    {'name': 'AI NI', 'full': 'AINI SURAYA BINTI HAMZAH', 'outlet': 'SU'},
    {'name': 'JOEN', 'full': 'TAN KANG ZHI', 'outlet': 'SU'},
    {'name': 'CORRINE', 'full': 'NG SIU ZHEN', 'outlet': 'SU'},
    {'name': 'CHERRY', 'full': 'CHERRY CHEE SHI HUI', 'outlet': 'SU'},
    {'name': 'JESSICA', 'full': 'LIONG ZI SHAN', 'outlet': 'SU'},
    {'name': 'KATHERINE', 'full': 'LAW RUI XUAN', 'outlet': 'SU'},
    {'name': 'QIAN BEI', 'full': 'LAU QIAN BEI', 'outlet': 'SU'},
    {'name': 'WEI XUAN', 'full': 'WONG WEI XUAN', 'outlet': 'SU'},
    {'name': 'DR MAX', 'full': 'KHOR YI ZHEN', 'outlet': 'SU'},
    {'name': 'DR ANN', 'full': 'ANN CHEW LIYEN', 'outlet': 'SU'},
    {'name': 'DR YI SHAN', 'full': 'CHONG YI SHAN', 'outlet': 'SU'},
    {'name': 'HESTER', 'full': 'WONG PIT KHI', 'outlet': 'KL'},
    {'name': 'ANGEL', 'full': 'ANGEL NG ANN QI', 'outlet': 'CL'},
    {'name': 'KETTY', 'full': 'HUANG XIAOFEN', 'outlet': 'CL'},
    {'name': 'ALICE', 'full': 'ALICE LEE', 'outlet': 'CL'},
    {'name': 'PINKY', 'full': 'CHONG LEE FONG', 'outlet': 'CL'},
    {'name': 'KAY YEE', 'full': 'CHIA KAY YEE', 'outlet': 'CL'},
    {'name': 'CASSIE', 'full': 'CASSIE HO YEN TONG', 'outlet': 'CL'},
    {'name': 'KAI WEI', 'full': 'NG KAI WEI', 'outlet': 'CL'},
    {'name': 'SHARON', 'full': 'FOOK ZHI XUAN', 'outlet': 'CL'},
    {'name': 'KATRINA', 'full': 'KATRINA SOON YONG QING', 'outlet': 'CL'},
    {'name': 'XIN YI', 'full': 'OH XIN YI', 'outlet': 'CL'},
    {'name': 'ELLIS', 'full': 'LEE AI LIS', 'outlet': 'CL'},
    {'name': 'ZI YING', 'full': 'THENG ZI YING', 'outlet': 'CL'},
    {'name': 'TAN HUI', 'full': 'TAN HUI', 'outlet': 'CL'},
    {'name': 'DR.RAINNIE', 'full': 'WONG HUI HUNG', 'outlet': 'CL'},
    {'name': 'DR.NATALIE', 'full': 'NATALIE KWONG ZHU WEN', 'outlet': 'CL'},
    {'name': 'DR SONIA', 'full': 'TEE PUI SIN', 'outlet': 'CL'},
    {'name': 'DR AGNES', 'full': 'AGNES LU', 'outlet': 'CL'},
    {'name': 'BETTY', 'full': 'BETTY SIA SIEW CHEE', 'outlet': 'PC'},
    {'name': 'RACHEL', 'full': 'KOK CHOY PEI', 'outlet': 'PC'},
    {'name': 'GINA', 'full': 'GOH SIEW GEK', 'outlet': 'PC'},
    {'name': 'SHUE BIN', 'full': 'LOW SHUE BIN', 'outlet': 'PC'},
    {'name': 'SU WEN', 'full': 'CHAI SU WEN', 'outlet': 'PC'},
    {'name': 'ZHI XIN', 'full': 'CHEONG ZEE YAN', 'outlet': 'PC'},
    {'name': 'WINNIE', 'full': 'WINNIE TING QIAN QIAN', 'outlet': 'PC'},
    {'name': 'AMANDA', 'full': 'AMANDA YII SIEW HIE', 'outlet': 'PC'},
    {'name': 'JOVEY', 'full': 'TAM SHING LIN', 'outlet': 'PC'},
    {'name': 'SANDY', 'full': 'NG KA HUI', 'outlet': 'PC'},
    {'name': 'DR.ZAELEY', 'full': 'CHAN SHIN YEE', 'outlet': 'PC'},
    {'name': 'DR.TAY', 'full': 'TAY SU YEE', 'outlet': 'PC'},
    {'name': 'DR JIN QIAN', 'full': 'LOO JIN QIAN', 'outlet': 'PC'},
    {'name': 'ATHENA', 'full': 'TEO HUI YOKE', 'outlet': 'SS2'},
    {'name': 'BERRY', 'full': 'KHOO CHIAO MEI', 'outlet': 'SS2'},
    {'name': 'SIM MEI', 'full': 'TANG SIM MEI', 'outlet': 'SS2'},
    {'name': 'VERON', 'full': 'CHOO YIN WEI', 'outlet': 'SS2'},
    {'name': 'JESSIE', 'full': 'LAU JIA CHYI', 'outlet': 'SS2'},
    {'name': 'TINA', 'full': 'ESTINA LAI BINTI ABDULLAH', 'outlet': 'SS2'},
    {'name': 'EN NING', 'full': 'YEONG EN NING', 'outlet': 'SS2'},
    {'name': 'CHING YUE', 'full': 'LIM CHING YUE', 'outlet': 'SS2'},
    {'name': 'WAN ROU', 'full': 'SIK WAN ROU', 'outlet': 'SS2'},
    {'name': 'WAN EN', 'full': 'YAN WAN EN', 'outlet': 'SS2'},
    {'name': 'YONG XIN', 'full': 'LEE YONG XIN', 'outlet': 'SS2'},
    {'name': 'DR. CAITLYN', 'full': 'LAU CHIN LING', 'outlet': 'SS2'},
    {'name': 'DR.TAN', 'full': 'TAN CZHIA HAO', 'outlet': 'SS2'},
    {'name': 'DR CASSANDRA', 'full': 'CHAN QING YAN', 'outlet': 'SS2'},
    {'name': 'DR CHIN WEI', 'full': 'KHOO CHIN WEI', 'outlet': 'SS2'},
    {'name': 'DR EUNICE', 'full': 'CHAN EUNICE', 'outlet': 'SS2'},
    {'name': 'DR WEN YUN', 'full': 'LOO WEN YUN', 'outlet': 'SS2'},
]

def find_participant(target_name):
    """Find participant by name. Extract name after hyphen and match."""
    name_part = target_name.split('-')[-1].strip().upper()
    for idx, p in enumerate(PARTICIPANTS):
        if name_part in p['name'].upper() or name_part in p['full'].upper():
            return idx
    return None

def main():
    print("🔥 FOL 2026 Angel's Whisper Importer")
    print("=" * 50)

    # Get CSV filename
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = input("CSV filename (or path): ").strip()

    # Get Firebase credentials file
    creds_file = input("Firebase credentials JSON file (or path): ").strip()

    if not creds_file or creds_file == "":
        print("❌ Firebase credentials file required!")
        print("   Get it from: Firebase Console → Project Settings → Service Accounts")
        return

    try:
        # Initialize Firebase
        print(f"🔐 Loading Firebase credentials from {creds_file}...")
        cred = credentials.Certificate(creds_file)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized")
    except Exception as e:
        print(f"❌ Firebase error: {e}")
        return

    try:
        # Read CSV
        print(f"📖 Reading CSV from {csv_file}...")
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            print("❌ No data rows in CSV")
            return

        print(f"✅ Loaded {len(rows)} rows")

        # Find column indices
        headers = rows[0].keys() if rows else []
        target_col = None
        message_col = None

        for col in headers:
            if '守护对象' in col or 'target' in col.lower():
                target_col = col
            if '想对TA说的话' in col or 'message' in col.lower():
                message_col = col

        if not target_col or not message_col:
            print(f"❌ Could not find target or message columns")
            print(f"   Available columns: {list(headers)}")
            return

        print(f"📋 Using columns: {target_col} → {message_col}")

        # Import
        imported = 0
        failed = 0

        for idx, row in enumerate(rows, 1):
            target = row.get(target_col, '').strip()
            message = row.get(message_col, '').strip()

            if not target or not message:
                print(f"  Row {idx}: ⊘ Missing target or message")
                failed += 1
                continue

            # Find participant
            p_idx = find_participant(target)
            if p_idx is None:
                print(f"  Row {idx}: ✗ '{target}' not found")
                failed += 1
                continue

            pid = f"P{str(p_idx + 1).zfill(3)}"
            p_name = PARTICIPANTS[p_idx]['name']

            # Save to Firebase
            try:
                db.collection('fol2026').document(pid).set({
                    'angelWhisper': message,
                    'angelRevealed': False
                }, merge=True)
                print(f"  Row {idx}: ✅ {target} → {p_name} ({pid})")
                imported += 1
            except Exception as e:
                print(f"  Row {idx}: ❌ Firebase error: {e}")
                failed += 1

        print("=" * 50)
        print(f"✅ Complete! Imported: {imported}, Failed: {failed}")

    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
