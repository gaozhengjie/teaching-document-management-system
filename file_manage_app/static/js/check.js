function validate_form() {
    if ($("#file_type").val() == "") {// 如果主体类型未选择
        alert("文件类型未选择!!!");
        $("#file_type").focus();
        return false;
    }
    return true;
}