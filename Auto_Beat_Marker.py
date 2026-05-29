import os
import sys
import site
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# --- રિઝોલ્વનો પાથ (API માટે) ---
resolve_module_path = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
if os.path.exists(resolve_module_path) and resolve_module_path not in sys.path:
    sys.path.append(resolve_module_path)

# --- પાયથોન લાઇબ્રેરીઓનો પાથ ---
for p in site.getsitepackages():
    if p not in sys.path:
        sys.path.append(p)
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.append(user_site)


class ModernBeatMarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Beat Marker Pro")
        self.root.geometry("550x380")
        self.root.configure(bg="#1e1e24")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        
        # UI વેરીએબલ્સ
        self.selected_track = tk.IntVar(value=1)
        self.custom_track_var = tk.StringVar(value="")
        
        self.build_ui()

    def build_ui(self):
        # ટાઇટલ
        title_lbl = tk.Label(self.root, text="AUTO BEAT MARKER", font=("Segoe UI", 20, "bold"), bg="#1e1e24", fg="#00a8ff")
        title_lbl.pack(pady=(20, 10))

        subtitle = tk.Label(self.root, text="Select Audio Track to analyze:", font=("Segoe UI", 11), bg="#1e1e24", fg="#cccccc")
        subtitle.pack()

        # ટ્રેક સિલેક્શન ફ્રેમ (1 થી 7 અને Other)
        self.track_frame = tk.Frame(self.root, bg="#1e1e24")
        self.track_frame.pack(pady=20)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Modern.TRadiobutton", background="#1e1e24", foreground="#ffffff", font=("Segoe UI", 12, "bold"), padding=10)
        style.map("Modern.TRadiobutton", foreground=[('selected', '#00a8ff')])

        for i in range(1, 8):
            rb = ttk.Radiobutton(self.track_frame, text=f" {i} ", variable=self.selected_track, value=i, style="Modern.TRadiobutton", command=self.hide_custom_entry)
            rb.grid(row=0, column=i-1, padx=5)

        rb_other = ttk.Radiobutton(self.track_frame, text="Other", variable=self.selected_track, value=99, style="Modern.TRadiobutton", command=self.show_custom_entry)
        rb_other.grid(row=0, column=7, padx=5)

        # કસ્ટમ નંબર નાખવા માટેનું બોક્સ (શરૂઆતમાં છુપાયેલું)
        self.custom_entry = tk.Entry(self.root, textvariable=self.custom_track_var, font=("Segoe UI", 12), bg="#2d2d34", fg="white", insertbackground="white", width=10, justify="center", relief="flat")
        
        # સ્ટાર્ટ બટન
        self.start_btn = tk.Button(self.root, text="START PROCESSING", font=("Segoe UI", 12, "bold"), bg="#00a8ff", fg="white", activebackground="#007acc", activeforeground="white", relief="flat", padx=30, pady=10, cursor="hand2", command=self.start_processing)
        self.start_btn.pack(pady=30)

        # પ્રોગ્રેસ UI (શરૂઆતમાં છુપાયેલું)
        self.progress_frame = tk.Frame(self.root, bg="#1e1e24")
        
        self.status_lbl = tk.Label(self.progress_frame, text="Initializing...", font=("Segoe UI", 12), bg="#1e1e24", fg="#00a8ff")
        self.status_lbl.pack(pady=(10, 5))
        
        # એડવાન્સ પ્રોગ્રેસ બાર
        style.configure("Modern.Horizontal.TProgressbar", thickness=15, background='#00a8ff', troughcolor='#2d2d34', bordercolor='#1e1e24', lightcolor='#00a8ff', darkcolor='#00a8ff')
        self.progress_bar = ttk.Progressbar(self.progress_frame, style="Modern.Horizontal.TProgressbar", orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.percent_lbl = tk.Label(self.progress_frame, text="0%", font=("Segoe UI", 14, "bold"), bg="#1e1e24", fg="white")
        self.percent_lbl.pack()

    def show_custom_entry(self):
        self.custom_entry.pack(pady=(0, 10))

    def hide_custom_entry(self):
        self.custom_entry.pack_forget()

    def update_progress(self, percent, text):
        # સ્મૂથ એનિમેશન અને લાઈવ અપડેટ માટે
        self.status_lbl.config(text=text)
        self.progress_bar["value"] = percent
        self.percent_lbl.config(text=f"{int(percent)}%")
        self.root.update_idletasks()

    def start_processing(self):
        # ટ્રેક નંબર નક્કી કરવો
        if self.selected_track.get() == 99:
            try:
                self.final_track = int(self.custom_track_var.get())
                if self.final_track <= 0: raise ValueError
            except:
                messagebox.showerror("Error", "કૃપા કરીને સાચો ટ્રેક નંબર લખો.")
                return
        else:
            self.final_track = self.selected_track.get()

        # UI બદલવું (બટન છુપાવી પ્રોગ્રેસ બાર બતાવવો)
        self.track_frame.pack_forget()
        self.start_btn.pack_forget()
        if self.selected_track.get() == 99: self.custom_entry.pack_forget()
        self.progress_frame.pack(pady=30)

        # થ્રેડિંગ (જેથી UI ચોંટી ન જાય)
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        self.update_progress(5, "Connecting to DaVinci Resolve API...")
        time.sleep(0.5)

        try:
            import DaVinciResolveScript as bmd
            resolve = bmd.scriptapp("Resolve")
            if not resolve: raise Exception("Resolve connection failed.")
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"API ભૂલ: {e}"))
            return

        self.update_progress(15, "Loading Python Libraries (Librosa & MoviePy)...")
        try:
            import librosa
            import numpy as np
            try:
                from moviepy import VideoFileClip
            except:
                from moviepy.editor import VideoFileClip
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Library ભૂલ: {e}"))
            return

        project_manager = resolve.GetProjectManager()
        current_project = project_manager.GetCurrentProject()
        timeline = current_project.GetCurrentTimeline()

        if not timeline:
            self.root.after(0, lambda: messagebox.showerror("Error", "પહેલા ટાઇમલાઇન ઓપન કરો."))
            self.root.after(0, self.root.destroy)
            return

        self.update_progress(25, f"Scanning Audio Track {self.final_track}...")
        audio_items = timeline.GetItemListInTrack("audio", self.final_track)
        
        if not audio_items:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Audio Track {self.final_track} પર કોઈ ક્લિપ મળી નથી."))
            self.root.after(0, self.root.destroy)
            return

        frame_rate = float(timeline.GetSetting("timelineFrameRate"))
        total_markers = 0
        
        # પ્રોસેસિંગ દરેક ક્લિપ માટે
        for idx, item in enumerate(audio_items):
            media_pool_item = item.GetMediaPoolItem()
            if not media_pool_item: continue
                
            file_path = media_pool_item.GetClipProperty("File Path")
            if not file_path or not os.path.exists(file_path): continue
                
            self.update_progress(35, f"File Found: {os.path.basename(file_path)}")
            audio_to_process = file_path
            temp_audio_path = None

            if file_path.lower().endswith(('.mp4', '.mov', '.mkv', '.avi')):
                self.update_progress(45, "Extracting Audio from Video File...")
                try:
                    video = VideoFileClip(file_path)
                    temp_audio_path = os.path.join(tempfile.gettempdir(), "temp_ext_audio.wav")
                    video.audio.write_audiofile(temp_audio_path, logger=None)
                    audio_to_process = temp_audio_path
                    video.close()
                except:
                    continue
            
            try:
                self.update_progress(60, "Analyzing Music Frequencies & Strength...")
                y, sr = librosa.load(audio_to_process)
                
                self.update_progress(75, "Detecting Beat Drops and Peaks...")
                onset_env = librosa.onset.onset_strength(y=y, sr=sr)
                max_env = np.max(onset_env) if np.max(onset_env) > 0 else 1
                
                onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, wait=10, delta=0.05)
                
                self.update_progress(90, "Applying Color-Coded Markers to Timeline...")
                start_frame = item.GetStart()
                left_offset = item.GetLeftOffset()
                end_frame = item.GetEnd()
                
                for frame in onset_frames:
                    strength = onset_env[frame] / max_env
                    t = librosa.frames_to_time(frame, sr=sr)
                    
                    if strength > 0.85: color, name = "Red", "Very High Beat"
                    elif strength > 0.60: color, name = "Yellow", "High Beat"
                    elif strength > 0.40: color, name = "Green", "Medium Beat"
                    elif strength > 0.20: color, name = "Cyan", "Low Beat"
                    else: color, name = "Blue", "Very Low Beat"

                    file_frame = int(t * frame_rate)
                    timeline_frame = start_frame + (file_frame - left_offset)
                    
                    if start_frame <= timeline_frame < end_frame:
                        try:
                            item.AddMarker(file_frame, color, name, f"Strength: {strength:.2f}", 1)
                        except:
                            timeline.AddMarker(timeline_frame, color, name, f"Strength: {strength:.2f}", 1)
                        total_markers += 1
                        
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
            finally:
                if temp_audio_path and os.path.exists(temp_audio_path):
                    try: os.remove(temp_audio_path)
                    except: pass

        self.update_progress(100, "Done! Process Complete.")
        time.sleep(0.5)
        
        def show_final_message():
            if total_markers > 0:
                messagebox.showinfo("Success 🎉", f"કુલ {total_markers} પ્રોફેશનલ કલર-કોડેડ માર્કર્સ લાગી ગયા છે!\n\nહવે તમે તમારો પ્રોજેક્ટ એડિટ કરી શકો છો.")
            else:
                messagebox.showwarning("No Beats", "મ્યુઝિકમાં કોઈ માર્કર લાગ્યા નથી.")
            self.root.destroy()
            
        self.root.after(0, show_final_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBeatMarkerApp(root)
    root.mainloop()