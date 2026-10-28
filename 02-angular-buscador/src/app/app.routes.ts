import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        redirectTo: '/home',
        pathMatch: 'full'
    },
    {
        path: 'home',
        loadChildren: () => import('./modules/libros/libros.routes').then(r => r.librosRoutes),
        title: 'Libros'
    },
 
];
