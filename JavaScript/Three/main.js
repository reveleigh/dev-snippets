import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene Setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a1a);
// Add some fog for depth
scene.fog = new THREE.Fog(0x1a1a1a, 10, 50);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true; // Enable shadows
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Lighting
const ambientLight = new THREE.AmbientLight(0x404040, 2); // Soft white light
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 50, 100);
pointLight.position.set(5, 5, 5);
pointLight.castShadow = true;
scene.add(pointLight);

const directionalLight = new THREE.DirectionalLight(0xff4d4d, 2); // Reddish light
directionalLight.position.set(-5, 5, 0);
scene.add(directionalLight);

// Objects (Torus Knot)
const geometry = new THREE.TorusKnotGeometry(10, 3, 100, 16);
const material = new THREE.MeshStandardMaterial({ 
    color: 0x00ff88,
    roughness: 0.2,
    metalness: 0.8,
});
const torusKnot = new THREE.Mesh(geometry, material);
torusKnot.scale.set(0.1, 0.1, 0.1);
torusKnot.castShadow = true;
torusKnot.receiveShadow = true;
scene.add(torusKnot);

// Floor
const floorGeometry = new THREE.PlaneGeometry(50, 50);
const floorMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x333333,
    roughness: 0.8,
    metalness: 0.2
});
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
floor.position.y = -2;
floor.receiveShadow = true;
scene.add(floor);

camera.position.z = 5;

// Animation Loop
function animate() {
    requestAnimationFrame(animate);

    // Rotate object
    torusKnot.rotation.x += 0.01;
    torusKnot.rotation.y += 0.01;

    // Update controls
    controls.update();

    renderer.render(scene, camera);
}

// Handle Window Resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();
