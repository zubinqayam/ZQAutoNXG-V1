// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;

#[cfg(not(debug_assertions))]
use tauri::api::process::{Command, CommandEvent};

fn main() {
  tauri::Builder::default()
    .setup(|app| {
        let window = app.get_window("main").unwrap();

        // In production, spawn the sidecar backend process.
        // In development, run the backend separately (e.g., `uvicorn zqautonxg.main:app --reload`).
        #[cfg(not(debug_assertions))]
        {
            match Command::new_sidecar("zqautonxg-backend")
                .and_then(|cmd| cmd.spawn())
            {
                Ok((mut rx, _child)) => {
                    tauri::async_runtime::spawn(async move {
                        while let Some(event) = rx.recv().await {
                            if let CommandEvent::Stdout(line) = event {
                                window
                                    .emit("message", Some(format!("'{}'", line)))
                                    .expect("failed to emit event");
                            }
                        }
                    });
                }
                Err(e) => {
                    eprintln!("Failed to spawn zqautonxg-backend sidecar: {}", e);
                }
            }
        }

        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
