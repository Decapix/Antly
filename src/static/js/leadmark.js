/*!
=========================================================
* LeadMark Landing page
=========================================================

*/

// smooth scroll
$(document).ready(function () {
  $(".navbar .nav-link").on("click", function (event) {
    if (this.hash !== "") {
      event.preventDefault();

      var hash = this.hash;

      $("html, body").animate(
        {
          scrollTop: $(hash).offset().top,
        },
        700,
        function () {
          window.location.hash = hash;
        }
      );
    }
  });
});

// protfolio filters
$(window).on("load", function () {
  var t = $(".portfolio-container");
  t.isotope({
    filter: ".new",
    animationOptions: {
      duration: 750,
      easing: "linear",
      queue: !1,
    },
  }),
    $(".filters a").click(function () {
      $(".filters .active").removeClass("active"), $(this).addClass("active");
      var i = $(this).attr("data-filter");
      return (
        t.isotope({
          filter: i,
          animationOptions: {
            duration: 750,
            easing: "linear",
            queue: !1,
          },
        }),
        !1
      );
    });
});

function submitFormSection(formSectionSelector) {
  var form = document.getElementById("my-form");
  var formSection = form.querySelector(formSectionSelector);
  form.submit();
}





/* function for detail image*/

function changeLargeImage(smallImage) {
  var largeImageImg = document.getElementById("large-image-img");
  var largeImageVideo = document.getElementById("large-image-video");
  if (smallImage.tagName === "IMG") {
    largeImageImg.src = smallImage.src;
    largeImageImg.style.display = "block";
    largeImageVideo.style.display = "none";
  } else if (smallImage.tagName === "VIDEO") {
    largeImageVideo.src = smallImage.src;
    largeImageVideo.style.display = "block";
    largeImageImg.style.display = "none";
    largeImageVideo.play();
  }
}


/* product page */

// Sélectionner tous les groupes de produits sur la page
const productGroups = document.querySelectorAll('.card-product-tri');

// Boucle sur chaque groupe de produits
productGroups.forEach(group => {
    // Compter le nombre d'éléments dans le groupe
    const count = group.querySelectorAll('#card-ele').length;

    // Ajouter la classe 'col-md-auto' ou 'col-md-4' en fonction du nombre d'éléments
    if (count < 3) {
        group.querySelector('#card-ele').classList.add('col-md-auto');
    } else {
        group.querySelectorAll('#card-ele').forEach(element => {
            element.classList.add('col-md-4');
        });
    }
});


// star comment color 

const starContainer = document.getElementById('star-container');
const stars = starContainer.querySelectorAll('.ti-star');
const starInput = document.querySelector('input[name="star"]');

function updateStars(value) {
    stars.forEach(star => {
        if (parseInt(star.dataset.value) <= value) {
            star.classList.add('star-filled');
        } else {
            star.classList.remove('star-filled');
        }
    });
    starInput.value = value;
}

stars.forEach(star => {
    star.addEventListener('click', () => {
        const value = parseInt(star.dataset.value);
        updateStars(value);
    });
});

updateStars(parseInt(starInput.value) || 5);