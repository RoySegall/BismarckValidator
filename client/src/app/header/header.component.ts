import {Component} from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'op-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  intro: any;

  constructor(private route: ActivatedRoute) {
    this.intro = null;
  }

  getIntro() {
    console.log(this.route);
    this.intro = introJs();
    let steps = [
      {
        element: document.querySelector('.dz-text'),
        intro: `גרור לפה קבצים או לחץ על התיבה על מנת לפתוח דיאלוג העלאת קבצים.`,
        position: 'right',
      }
    ];

    if (document.querySelector('#checkFiles')) {
      steps.push({
        element: document.querySelector('#checkFiles'),
        intro: `בעת לחיצה על הכפתור תהליך הבדיקה יתחיל.`,
        position: 'right',
      })
    }
    this.intro.setOptions({
      nextLabel: 'המשך >>',
      prevLabel: '<< חזור',
      skipLabel: '',
      doneLabel: 'סגור',
      steps: steps
    });
    return this.intro;
  }

  startIntro() {
    const intro = this.getIntro();
    intro.start();
  }

}
