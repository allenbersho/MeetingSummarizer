gsap.registerPlugin(ScrollTrigger);

gsap.to("#stars", { 
    x: 100, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});

gsap.to("#moon", { 
    y: -100, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});

gsap.to("#mountback", { 
    y: -50, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});

gsap.to("#mountfront", { 
    y: 50, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});

gsap.to("#text", { 
    x: -850, 
    y: 150, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});

gsap.to("#btn", { 
    y: 50, 
    duration: 3, 
    ease: "power1.out", 
    scrollTrigger: { scrub: 1 } 
});


document.addEventListener("mousemove", (e) => {
    const cursor = document.querySelector(".custom-cursor");
    cursor.style.left = `${e.clientX}px`;
    cursor.style.top = `${e.clientY}px`;
  });

  document.addEventListener("DOMContentLoaded", function () {
    gsap.registerPlugin(ScrollTrigger);
    gsap.from(".terminal-left", {
      scrollTrigger: {
        trigger: ".terminal-left",
        start: "top 80%",
        toggleActions: "play none none none"
      },
      opacity: 0,
      x: -50,
      duration: 1.2
    });
    
    gsap.from(".terminal-right", {
      scrollTrigger: {
        trigger: ".terminal-right",
        start: "top 80%",
        toggleActions: "play none none none"
      },
      opacity: 0,
      x: 50,
      duration: 1.2
    });
  });