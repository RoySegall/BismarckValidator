import { Component } from '@angular/core';

@Component({
  selector: 'op-root',
  template: `
    <op-header></op-header>
    <div id="app-wrapper">
      <router-outlet></router-outlet>
    </div>
    <op-footer></op-footer>
  `,
  styles: [`
    #app-wrapper {
      width: 98%;
      margin: auto;
      height: 79vh;
    }
  `],
})
export class OpComponent {
}
