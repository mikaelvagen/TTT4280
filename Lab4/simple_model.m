load('muab.mat');


red_wavelength = 600; % (unit nm)
green_wavelength = 515; % (unit nm)
blue_wavelength = 460; % (unit nm)

wavelengths = [red_wavelength, green_wavelength, blue_wavelength];

mua_blood_oxy = @(x) interp1(muabo(:,1), muabo(:,2), x);
mua_blood_deoxy = @(x) i\\nterp1(muabd(:,1), muabd(:,2), x);


bvf = 0.01; % blood volume fraction, average amount of blood in the tissue
oxy = 0.8; % oxygenation of the blood

% absorption coefficient (mu_a in lab text)
% units: m^(-1)
mua_other = 25; %background absorption due to collagen etc
mua_blood = mua_blood_oxy(wavelengths)*oxy + mua_blood_deoxy(wavelengths)*(1-oxy); %absorption due to pure blood
mua = mua_blood*bvf + mua_other;

% reduced scattering coefficient (mu_s' in lab text)
% the magic numbers are from N. Bashkatov, E. A. Genina, V. V. Tuchin.
% Optical properties of skin, subcutaneous and muscle tissues: A review. J.
% Inoov.  Opt. Health Sci., 4(1):9-38, 2011
% units: m^(-1)
musr = (17.6*(wavelengths/500.0).^(-4) + 18.78*(wavelengths/500).^(-0.22))*100;

% mua and musr are now available as three-valued arrays, each index corresponding to: red, green and blue channels.


% calculating penetration depth:
p_depth_red = sqrt(1 / (3 * (musr(1) + mua(1)) * mua(1))); % unit m
p_depth_green = sqrt(1 / (3 * (musr(2) + mua(2)) * mua(2))); % unit m
p_depth_blue = sqrt(1 / (3 * (musr(3) + mua(3)) * mua(3))); % unit m

p_depth = [p_depth_red, p_depth_green, p_depth_blue];

% fprintf("Penetration depth at wavelength of 600nm: %.2f nm.\n", p_depth_red)
% fprintf("Penetration depth at wavelength of 515nm: %.2f nm.\n", p_depth_green)
% fprintf("Penetration depth at wavelength of 460nm: %.2f nm.\n", p_depth_blue)

% calculating bvf 100% and bvf 1%:
diameter = 300e-6;
bvf_vein = 1; % 100%
mua_vein = mua_blood * bvf_vein + mua_other;
new_p_depth = sqrt(1 ./ (3 .* (musr + mua_vein) .* mua_vein));
C = sqrt(3 .* (musr + mua) .* mua);
C_2 = sqrt(3 .* (musr + mua_vein) .* mua_vein);

T_vein = exp(-C_2 .* diameter);
T_tissue = exp(-C .* diameter);

K = abs(T_vein - T_tissue) ./ T_tissue;




