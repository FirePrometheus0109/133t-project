export class CheckBoxHelper {

  public checkBoxName: string;
  constructor(checkBoxName: string) {
    this.checkBoxName = checkBoxName;
  }

  public selectAllCheckboxes() {
    const allCheckboxes = this.getAllCheckboxes();
    allCheckboxes.forEach((checkbox) => {
      checkbox.click();
    });
  }

  private getAllCheckboxes(checked: boolean = false): NodeListOf<HTMLInputElement> {
    const isChecked = (checked) ? ':checked' : '';
    // Array.prototype.slice.call() used for compatibility with IE
    return Array.prototype.slice.call(document.querySelectorAll(`input[name="${this.checkBoxName}"]${isChecked}`));
  }

  public getAllSelectedItems(): number[] {
    const allCheckedArray: object[] = Array.prototype.slice.call(this.getAllCheckboxes(true));
    return allCheckedArray.map(a => +a['value']);
  }
}
