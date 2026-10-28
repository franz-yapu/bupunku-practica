import { Component, inject, OnInit } from '@angular/core';
import { LibrosService,LibrosResponse } from './libros.service';

@Component({
  imports: [],
  selector: 'app-libros',
  styleUrl: './libros.css',
  templateUrl: './libros.html',
})
export class Libros implements OnInit {
   private service: LibrosService = inject(LibrosService);
   public librosData: LibrosResponse = {
    numFound: 0,
    start: 0,
    docs: []
  };

constructor( ) {}

  ngOnInit() {
    this.getlibros();
    this.getlibros2();
  }

  getlibros() {
    this.service.getLibros().then((data: LibrosResponse) => {
        this.librosData = data;
        console.log('Libros data:', data);
    }).catch((error) => {
        console.error('Error fetching libros:', error);
    });
  }


  getlibros2() {
    this.service.getLibros2().subscribe({
        next: (data: LibrosResponse) => {
            this.librosData = data;
            console.log('Libros data (Observable):', data);
        },
        error: (error) => {
            console.error('Error fetching libros (Observable):', error);
        }
    });
  }





}