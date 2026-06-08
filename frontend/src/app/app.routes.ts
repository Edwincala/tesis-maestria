import { Routes } from '@angular/router';
import {DashboardComponent} from './features/dashboard/pages/dashboard/dashboard';
import { MainLayout } from './shared/layouts/main-layout/main-layout';
import { MeasurementsHistory } from './features/measurements/pages/measurements-history/measurements-history';
import { Login } from './features/auth/pages/login/login';

export const routes: Routes = [
    {
        path: '',
        component: MainLayout,
        children: [
            {
                path: '',
                redirectTo: 'dashboard',
                pathMatch: 'full'
            },
            {
                path: 'dashboard',
                component: DashboardComponent
            },
            {
                path: 'measurements',
                component: MeasurementsHistory
            },
            {
                path: 'login',
                component: Login
            }
        ]
    },
    {
        path: '**',
        redirectTo: 'dashboard'
    }
];
