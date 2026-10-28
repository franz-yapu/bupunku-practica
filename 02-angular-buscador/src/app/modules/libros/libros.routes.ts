import { Routes } from "@angular/router";



export const librosRoutes: Routes = [

    {
        path: '',
        loadComponent: () => import('./libros').then(c => c.Libros),
        title: 'Libros'
    }
    
]