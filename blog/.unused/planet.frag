#ifdef GL_ES
precision mediump float;
#endif

#define RADIUS 1.000
#define PIXEL_RESOLUTION 90.
#define BASE_COLOR vec4(1.)
#define SIZE 5.
#define OCTAVES 6
#define SPEED 0.01

#define RGB_BG vec3(235.,104.,100.)
#define BG_COLOR vec3(RGB_BG.r/255.,RGB_BG.g/255.,RGB_BG.b/255.)
#define HIGH_COLOR vec3(0.273,0.760,0.140)
#define MED_COLOR vec3(0.252,0.865,0.183)
#define LOW_COLOR vec3(0.440,0.505,0.960)

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float rand(vec2 coord) {
	coord = mod(coord, floor(vec2(2.0,1.0)*SIZE));
	return fract(sin(dot(coord.xy ,vec2(12.9898,78.233))) * 15.5453);
}

float noise(vec2 coord){
	vec2 i = floor(coord);
	vec2 f = fract(coord);
		
	float a = rand(i);
	float b = rand(i + vec2(1.0, 0.0));
	float c = rand(i + vec2(0.0, 1.0));
	float d = rand(i + vec2(1.0, 1.0));

	vec2 cubic = f * f * (3.0 - 2.0 * f);

	return mix(a, b, cubic.x) + (c - a) * cubic.y * (1.0 - cubic.x) + (d - b) * cubic.x * cubic.y;
}

float fbm(vec2 coord){
	float value = 0.0;
	float scale = 0.5;

	for(int i = 0; i < OCTAVES ; i++){
		value += noise(coord) * scale;
		coord *= 2.0;
		scale *= 0.5;
	}
	return value;
}

vec2 spherify(vec2 uv) {
    float z = sqrt(RADIUS - dot(uv, uv));
    vec2 sphere = uv/(z + RADIUS);
    return sphere;
}

float dither(vec2 uv1, vec2 uv2) {
    return (mod(uv1.x+uv2.y,2.0/PIXEL_RESOLUTION) <= 1.0 / PIXEL_RESOLUTION) ? 0.6 : 0.0;
}

void main() {
    // center
    vec2 st = gl_FragCoord.xy / u_resolution;
    vec2 uv = st;
    
    st = st*2.-1.;
    uv = uv*2.-1.;
    
    // pixelize
    uv = floor(uv * PIXEL_RESOLUTION) / PIXEL_RESOLUTION;
    
    // get dither
    float dith = dither(uv, st);
    
    // fix aspect ratio
    uv.x *= u_resolution.x / u_resolution.y;
    
    float d = distance(uv, vec2(0.0));
    // spherify
    uv = spherify(uv);
    
    vec3 color = LOW_COLOR;
    float n = fbm(uv * SIZE + u_time * SPEED);
    if (n > 0.6) {
        color = HIGH_COLOR;
    } else if (n > 0.4) {
        color = MED_COLOR;
    }
    
    // clouds
    float cloudn = mix(fbm(uv * SIZE + u_time*(SPEED*1.0015)), fbm(uv * SIZE + u_time*(SPEED*1.0001)), sin(fbm(fbm(uv*SIZE)*uv*2. * SIZE + u_time*0.01)/10.));
    
    // circle stencil
    float a = 1.-step(RADIUS, d);
    
    // lighting
    vec2 lightpos = vec2(0.3,0.3);
    vec2 mousepos = (u_mouse/u_resolution)*2.-1.;
    if (u_mouse.x <= u_resolution.x*0.99 && u_mouse.x >= u_resolution.x*.01 && u_mouse.y >= u_resolution.y*.01 && u_mouse.y <= u_resolution.y*.99) {
        lightpos = mousepos;
    	lightpos.x *= u_resolution.x/u_resolution.y;
    }
    
    float lightd = distance(uv, lightpos);
    if (cloudn > 0.522 && cloudn < 0.928)  {
        a -= 0.6 * step(0.9, lightd);
        
    } else {
        if (lightd >= 0.85) {
    		a -= 0.6;
        } else {
            // cloud shadow
    		vec2 offset = lightpos/10.;
    		float shadown = mix(fbm((uv+offset) * SIZE + u_time*(SPEED*1.0015)), fbm((uv+offset) * SIZE + u_time*(SPEED*1.0001)), sin(fbm(fbm(uv*SIZE)*uv*2. * SIZE + u_time*0.01)/10.));
            if (shadown > 0.5 && shadown < 0.8) color = mix(color, vec3(0.), 0.2);
        }
        if (lightd >= 0.830 && lightd < 0.85) { 
            a -=  dith; 
        }
    }
    
    if (cloudn > 0.522 && cloudn < 0.8) color = mix(color, vec3(1.), 1.);
    
    gl_FragColor = vec4(mix(vec3(0.), color, a), 1.);
    if (a==0.) gl_FragColor = vec4(BG_COLOR, 1.);
}
