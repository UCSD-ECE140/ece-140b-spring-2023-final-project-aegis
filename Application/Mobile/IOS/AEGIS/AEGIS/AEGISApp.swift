//
//  AEGISApp.swift
//  AEGIS
//
//  Created by Emin Tunc Kirimlioglu on 6/5/23.
//
//

import SwiftUI

@main
struct AEGISApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
