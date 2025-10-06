function CheckFirmType(val) {
    var write_about_business_div = document.getElementById('write_about_business_div');
    if (val == 'Other') {
        write_about_business_div.style.display = 'block';
    } else {
        write_about_business_div.style.display = 'none';
    }
}

function CheckRegType(regTypeVal) {
    var firm_type_div = document.getElementById('firm_type_div');
    var firm_regtype_div = document.getElementById('firm_regtype_div');

    var companydoc_div = document.getElementById('companydoc_div');

    var registration_certificate_div = document.getElementById('registration_certificate_div');
    var docinfo_div = document.getElementById('docinfo_div');

    var doc_type = document.getElementById('doc_type');

    if (regTypeVal === 'Other' || regTypeVal === 'Not Registered') {
        firm_type_div.classList.remove('col-md-6');
        firm_type_div.classList.add('col-md-3');

        firm_regtype_div.classList.remove('col-md-6');
        firm_regtype_div.classList.add('col-md-4');

        companydoc_div.style.display = 'block';
        docinfo_div.style.display = 'block';
        registration_certificate_div.style.display = 'none';
    } else if (regTypeVal == '') {
        firm_type_div.classList.remove('col-md-3');
        firm_type_div.classList.add('col-md-6');

        firm_regtype_div.classList.remove('col-md-4');
        firm_regtype_div.classList.add('col-md-6');

        companydoc_div.style.display = 'none';
        registration_certificate_div.style.display = 'none';
        docinfo_div.style.display = 'none';

    } else {
        firm_type_div.classList.remove('col-md-6');
        firm_type_div.classList.add('col-md-3');

        firm_regtype_div.classList.remove('col-md-6');
        firm_regtype_div.classList.add('col-md-4');

        companydoc_div.style.display = 'block';
        registration_certificate_div.style.display = 'block';
        docinfo_div.style.display = 'none';

        // Reset by setting to empty value (if that option exists)
        doc_type.value = '';

        // OR forcefully set the first option
        doc_type.selectedIndex = 0;

        // Optional: trigger change event if needed
        doc_type.dispatchEvent(new Event('change'));
    }
}

function CheckTaxType(regTaxVal) {
    var tax_type_div = document.getElementById('tax_type_div');

    var gstnumber_div = document.getElementById('gstnumber_div');
    var gstcertificate_div = document.getElementById('gstcertificate_div');

    if (regTaxVal === 'GST') {
        tax_type_div.classList.remove('col-md-12');
        tax_type_div.classList.add('col-md-3');

        gstnumber_div.style.display = 'block';
        gstcertificate_div.style.display = 'block';
    } else {
        tax_type_div.classList.remove('col-md-3');
        tax_type_div.classList.add('col-md-12');

        gstnumber_div.style.display = 'none';
        gstcertificate_div.style.display = 'none';
    }
}

function CheckDocType(docTypeVal) {
    var pancard_div = document.getElementById('pancard_div');
    var aadhaarcard_div = document.getElementById('aadhaarcard_div');

    if (docTypeVal === 'PAN') {
        pancard_div.style.display = 'block';
        aadhaarcard_div.style.display = 'none';
    } else if (docTypeVal === 'AADHAAR') {
        pancard_div.style.display = 'none';
        aadhaarcard_div.style.display = 'block';
    } else {
        pancard_div.style.display = 'none';
        aadhaarcard_div.style.display = 'none';
    }
}

function checkCountry(countryId) {
    var url = $('#country').data('url'); // ✅ get the Django-generated URL
    if (countryId && url) {
        $.ajax({
            url: url,
            data: {
                'country_id': countryId
            },
            success: function(data) {
                var stateDropdown = $('#state');
                stateDropdown.prop('disabled', false);
                stateDropdown.empty().append('<option value="">Select State</option>');

                $.each(data, function(index, state) {
                    stateDropdown.append('<option value="' + state.id + '">' + state.name + '</option>');
                });
            }
        });
    } else {
        var cityDropdown = $('#state');
        cityDropdown.prop('disabled', true).empty().append('<option value="">Select State</option>');
    }
}

function checkState(stateId) {
    var url = $('#state').data('url'); // ✅ get the Django-generated URL
    if (stateId && url) {
        $.ajax({
            url: url,
            data: {
                'state_id': stateId
            },
            success: function(data) {
                var cityDropdown = $('#city');
                cityDropdown.prop('disabled', false);
                cityDropdown.empty().append('<option value="">Select City</option>');

                $.each(data, function(index, city) {
                    cityDropdown.append('<option value="' + city.id + '">' + city.name + '</option>');
                });
            }
        });
    } else {
        var cityDropdown = $('#city');
        cityDropdown.prop('disabled', true).empty().append('<option value="">Select City</option>');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("companyForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            const allFields = this.querySelectorAll('[required]');
            allFields.forEach(field => {
                const style = window.getComputedStyle(field);
                const isHidden = (field.offsetParent === null || style.display === 'none' || style.visibility === 'hidden');

                if (isHidden) {
                    field.removeAttribute('required');
                }
            });
        });
    }
});
