'use strict';



/**
 * Mobile navbar toggle
 */

const navbar = document.querySelector("[data-navbar]");
const navToggler = document.querySelector("[data-nav-toggler]");

navToggler.addEventListener("click", function () {
  navbar.classList.toggle("active");
});



/**
 * Header active
 */

const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {
  header.classList[this.scrollY > 50 ? "add" : "remove"]("active");
});
/**
 * Form
 */

function openContactForm() {
  const overlay = document.getElementById('overlayContactForm');
  overlay.style.display = 'flex';
}

document.getElementById('contactUsBtn').addEventListener('click', function(event) {
  event.preventDefault(); 
  openContactForm(); 
});

function closeContactForm() {
  const overlay = document.getElementById('overlayContactForm');
  overlay.style.display = 'none'; 
}

$(document).ready(function() {
  $('#contactForm').submit(function(event) {
      event.preventDefault(); 

      $.ajax({
          type: 'POST',
          url: $(this).attr('action'), 
          data: $(this).serialize(), 
          success: function(response) {
              $('#responseMessage').html(response); 
              $('#contactForm')[0].reset(); 
          },
          error: function() {
              $('#responseMessage').html('There was an error submitting the form.'); 
          }
      });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const blogPosts = document.querySelectorAll('.blog-post');
  blogPosts.forEach((post, index) => {
      post.style.animationDelay = `${index * 0.2}s`; 
  });
});