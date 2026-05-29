```python
import os
import sys

# DaVinci Resolve API સેટઅપ
def get_resolve():
    try:
        import DaVinciResolveScript as bmd
        return bmd.scriptapp("Resolve")
    except ImportError:
        print("ભૂલ: DaVinci Resolve Scripting API મળ્યું નથી.")
        return None

try:
    import librosa
except ImportError:
    print("ભૂલ: મ્યુઝિક એનાલિસિસ માટે 'librosa' લાઇબ્રેરી ઇન્સ્ટોલ કરો. (pip install librosa)")
    sys.exit()

def add_beat_markers(audio_path):
    resolve = get_resolve()
    if not resolve:
        return

    project_manager = resolve.GetProjectManager()
    current_project = project_manager.GetCurrentProject()
    timeline = current_project.GetCurrentTimeline()

    if not timeline:
        print("ભૂલ: પ્રોજેક્ટમાં કોઈ એક્ટિવ ટાઇમલાઇન મળી નથી!")
        return

    print("મ્યુઝિક ટ્રેક એનાલાઇઝ થઈ રહ્યો છે... થોડી રાહ જુઓ...")
    
    # મ્યુઝિકમાંથી બીટ શોધવી
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # ટાઇમલાઇનનો ફ્રેમ રેટ મેળવવો
    frame_rate = float(timeline.GetSetting("timelineFrameRate"))
    
    print(print(f"ટોટલ {len(beat_times)} બીટ્સ મળી. માર્કર્સ ઉમેરાઈ રહ્યા છે..."))

    # Resolve ની ટાઇમલાઇન પર માર્કર ઉમેરવા
    for t in beat_times:
        # સેકન્ડને ફ્રેમમાં કન્વર્ટ કરવું
        frame = int(t * frame_rate)
        
        # માર્કર ઉમેરવાનો કમાન્ડ (FrameNum, Color, Name, Note, Duration)
        timeline.AddMarker(frame, "Blue", "Beat", "Auto Generated", 1)

    print("સફળતાપૂર્વક બધા બીટ માર્કર્સ લાગી ગયા છે! 🎉")

if __name__ == "__main__":
    # અહીં તમારા ઓડિયો ફાઇલનો સાચો પાથ (Path) નાખો
    AUDIO_FILE = "C:/Users/YourName/Music/audio.wav" 
    
    if os.path.exists(AUDIO_FILE):
        add_beat_markers(AUDIO_FILE)
    else:
        print("આપેલ ઓડિયો ફાઇલ મળી નથી. કૃપા કરીને સાચો પાથ ચેક કરો.")