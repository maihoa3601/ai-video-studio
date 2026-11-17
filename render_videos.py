import subprocess
import json
from pathlib import Path

video_src = r"C:\Users\ADMIN\.gemini\antigravity\brain\5ea9e4f9-9315-46c1-a47d-fa8b22b0de11\.user_uploaded\media_1794922866995_7b5cf639.mp4"
bgm_src = r"ai-tiktok-factory\assets\music\background.mp3"

def get_dur(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(f)], capture_output=True, text=True)
    return float(json.loads(r.stdout)['format']['duration'])

configs = [
    {
        'voice': 'voice_playful_witty.mp3',
        'with_bgm': True,
        'output': 'video_long_tieng_hai_huoc_kem_nhac.mp4'
    },
    {
        'voice': 'voice_playful_witty.mp3',
        'with_bgm': False,
        'output': 'video_long_tieng_hai_huoc_khong_nhac.mp4'
    },
    {
        'voice': 'voice_chipmunk.mp3',
        'with_bgm': True,
        'output': 'video_long_tieng_chipmunk_meme.mp4'
    },
    {
        'voice': 'voice_nu_hai_huoc.mp3',
        'with_bgm': True,
        'output': 'video_long_tieng_nu_vui_nhon.mp4'
    }
]

for cfg in configs:
    dur = get_dur(cfg['voice'])
    out_audio = 'tmp_audio_' + cfg['output'] + '.mp3'
    if cfg['with_bgm']:
        fade_start = max(0.0, dur - 2.0)
        cmd_a = [
            'ffmpeg', '-y',
            '-i', cfg['voice'],
            '-i', bgm_src,
            '-filter_complex',
            f'[1:a]volume=0.12,afade=t=out:st={fade_start:.2f}:d=2.0[bg];[0:a][bg]amix=inputs=2:duration=first[out]',
            '-map', '[out]',
            out_audio
        ]
        subprocess.run(cmd_a, check=True)
    else:
        out_audio = cfg['voice']
        
    cmd_v = [
        'ffmpeg', '-y',
        '-stream_loop', '-1',
        '-i', video_src,
        '-i', out_audio,
        '-t', f'{dur:.3f}',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-c:a', 'aac', '-b:a', '192k',
        cfg['output']
    ]
    subprocess.run(cmd_v, check=True)
    print(f"Successfully rendered: {cfg['output']} (duration: {dur:.2f}s)")

print("ALL RENDERS COMPLETED SUCCESSFULLY!")
