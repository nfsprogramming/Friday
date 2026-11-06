/**
 * FRIDAY — Main entry point.
 *
 * Wires together the orb visualization and LiveKit voice pipeline.
 */

import { Room, RoomEvent, RemoteParticipant, RemoteTrack, Track } from "livekit-client";
import { createOrb, type OrbState } from "./orb";
import "./style.css";

// ---------------------------------------------------------------------------
// State machine
// ---------------------------------------------------------------------------

type State = "idle" | "listening" | "thinking" | "speaking";
let currentState: State = "idle";
let isMuted = false;

const statusEl = document.getElementById("status-text")!;
const errorEl = document.getElementById("error-text")!;

function showError(msg: string) {
  errorEl.textContent = msg;
  errorEl.style.opacity = "1";
  setTimeout(() => {
    errorEl.style.opacity = "0";
  }, 5000);
}

function updateStatus(state: State) {
  const labels: Record<State, string> = {
    idle: "",
    listening: "listening...",
    thinking: "thinking...",
    speaking: "speaking...",
  };
  statusEl.textContent = labels[state];
}

// ---------------------------------------------------------------------------
// Init components
// ---------------------------------------------------------------------------

const canvas = document.getElementById("orb-canvas") as HTMLCanvasElement;
const orb = createOrb(canvas);

// We need an AudioContext to analyze the remote audio track
let audioContext: AudioContext | null = null;
let analyser: AnalyserNode | null = null;
let room: Room | null = null;

function initAudio() {
  if (audioContext) return;
  audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  analyser = audioContext.createAnalyser();
  analyser.fftSize = 512;
  orb.setAnalyser(analyser);
}

function transition(newState: State) {
  if (newState === currentState) return;
  currentState = newState;
  orb.setState(newState as OrbState);
  updateStatus(newState);
}

// ---------------------------------------------------------------------------
// LiveKit Room Connection
// ---------------------------------------------------------------------------

async function connectToLiveKit() {
  try {
    const response = await fetch("/api/token");
    if (!response.ok) {
      throw new Error("Failed to fetch token from /api/token");
    }
    const data = await response.json();
    
    room = new Room({
      adaptiveStream: true,
      dynacast: true,
    });

    // Handle incoming audio tracks (FRIDAY's voice)
    room.on(RoomEvent.TrackSubscribed, (track: RemoteTrack, publication, participant: RemoteParticipant) => {
      if (track.kind === Track.Kind.Audio) {
        // Attach track to a standard HTMLAudioElement
        const audioElement = track.attach();
        document.body.appendChild(audioElement);

        // Analyze audio for the orb
        if (audioContext && analyser) {
          try {
            const source = audioContext.createMediaStreamSource(track.mediaStream!);
            source.connect(analyser);
            // DO NOT connect analyser to destination, as the HTMLAudioElement is already playing it
          } catch(e) {
            console.error("Error creating audio source:", e);
          }
        }
      }
    });

    room.on(RoomEvent.ActiveSpeakersChanged, (speakers) => {
      // If the agent is speaking, switch to speaking state
      const agentSpeaking = speakers.some(p => p !== room?.localParticipant);
      if (agentSpeaking) {
        transition("speaking");
      } else {
        transition("listening");
      }
    });

    await room.connect(data.serverUrl, data.token);
    console.log("Connected to LiveKit room:", room.name);
    
    // Enable microphone
    await room.localParticipant.enableCameraAndMicrophone();
    transition("listening");

  } catch (err: any) {
    console.error("LiveKit connection error:", err);
    showError("Could not connect to FRIDAY backend: " + err.message);
  }
}

// ---------------------------------------------------------------------------
// Kick off
// ---------------------------------------------------------------------------

// Resume AudioContext on ANY user interaction (browser autoplay policy)
function ensureAudioContext() {
  initAudio();
  if (audioContext?.state === "suspended") {
    audioContext.resume().then(() => console.log("[audio] context resumed"));
  }
}

document.addEventListener("click", () => {
  ensureAudioContext();
  if (!room) {
    statusEl.textContent = "connecting...";
    connectToLiveKit();
  }
});
document.addEventListener("touchstart", ensureAudioContext);
document.addEventListener("keydown", ensureAudioContext, { once: true });

// Try to resume audio context on load
ensureAudioContext();

// ---------------------------------------------------------------------------
// UI Controls
// ---------------------------------------------------------------------------

const btnMute = document.getElementById("btn-mute")!;
// We've hidden/removed menu controls for FRIDAY
btnMute.addEventListener("click", (e) => {
  e.stopPropagation();
  isMuted = !isMuted;
  btnMute.classList.toggle("muted", isMuted);
  if (room && room.localParticipant) {
    room.localParticipant.setMicrophoneEnabled(!isMuted);
  }
  if (isMuted) {
    transition("idle");
  } else {
    transition("listening");
  }
});

// Hide Jarvis specific buttons in the HTML
const menuDropdown = document.getElementById("menu-dropdown");
if (menuDropdown) menuDropdown.style.display = "none";
const btnMenu = document.getElementById("btn-menu");
if (btnMenu) btnMenu.style.display = "none";

