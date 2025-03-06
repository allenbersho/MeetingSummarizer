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