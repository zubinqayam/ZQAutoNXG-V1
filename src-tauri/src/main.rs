// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::api::process::{Command, CommandEvent};
use tauri::Manager;

fn main() {
  tauri::Builder::default()
    .setup(|app| {
        // This is where we would start the sidecar
        // For development, we usually run the backend separately
        // But in production, we'd spawn the sidecar here

        let window = app.get_window("main").unwrap();

        // Example of starting a sidecar (needs configuration in tauri.conf.json)

        let (mut rx, _child) = Command::new_sidecar("zqautonxg-backend")
            .expect("failed to create `zqautonxg-backend` binary command")
            .spawn()
            .expect("Failed to spawn sidecar");

        tauri::async_runtime::spawn(async move {
            // read events such as stdout
            while let Some(event) = rx.recv().await {
                if let CommandEvent::Stdout(line) = event {
                    window
                        .emit("message", Some(format!("'{}'", line)))
                        .expect("failed to emit event");
                }
            }
        });


        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
