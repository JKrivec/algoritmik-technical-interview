import toastr from "toastr";
import "toastr/build/toastr.min.css";

function use_toastr() {
    toastr.options.positionClass = "toast-bottom-right";
    toastr.options.closeButton = true;
    toastr.options.progressBar = true;

    return toastr;
}

export { use_toastr };
