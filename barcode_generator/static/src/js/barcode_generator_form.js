/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { useEffect } from "@web/core/utils/hooks";

export class BarcodeFormController extends FormController {
    setup() {
        super.setup();
        useEffect(() => {
            const handleKeyDown = (ev) => {
                if (ev.key === 'Enter' && !ev.shiftKey) {
                    const currentElement = document.activeElement;
                    let nextElement;

                    // Urutan field sesuai dengan ID-nya
                    const fieldOrder = ['fname', 'fdf', 'fdt', 'fbt', 'fpr'];
                    const currentIndex = fieldOrder.indexOf(currentElement.id);

                    // Jika elemen ditemukan dalam fieldOrder, pindahkan fokus ke elemen berikutnya
                    if (currentIndex !== -1 && currentIndex < fieldOrder.length - 1) {
                        nextElement = document.getElementById(fieldOrder[currentIndex + 1]);
                        if (nextElement) {
                            ev.preventDefault();
                            nextElement.focus(); // Fokuskan elemen berikutnya
                        }
                    }
                }
            };

            // Tambahkan event listener untuk keydown pada dokumen
            document.addEventListener('keydown', handleKeyDown);

            // Menghapus event listener ketika komponen dibersihkan
            return () => {
                document.removeEventListener('keydown', handleKeyDown);
            };
        });
    }
}
