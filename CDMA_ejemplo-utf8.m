%% Ejemplo CDMA

clc
clear all
close all

% Parámetros

n_data = 3;     % nro bits de datos
n_PN = 30;       % nro de bits secuencia pseudo aleatoria
n = 2;          % cantidad de usuarios simultaneos 

%% Generacion de datos

% generacion de datos y las secuencias pseudo aleatorias para la
% codificacion
data = randi([0 1],n_data,n);
PN = randi([0 1],n_PN,n);

for i = 1:n
    disp(strcat("Data usuario ",i))
    transpose(data(:,i))
end
for i = 1:n
    disp(strcat("Secuencia pseudoaleatoria usuario ",i))
    transpose(PN(:,i))
end
%% Codificacion
% 
% codificacion
data = 2*data-1;

for i = 1:n
    signal(:,i) = kron(data(:,i),PN(:,i));
end
signal
%%
% concatena la secuencia PN n_data veces
PN_long = repmat(PN,[n_data 1]);

% repite los datos para graficar
PN_mat_plot = repelem(PN_long,100,1);
data_plot = repelem(data,100,1);
signal_plot = repelem(signal,100,1);

L=length(PN_mat_plot);


for user = 1:n
    figure
    subplot(3,1,1)
    plot(data_plot(:,user),'linewidth',3)
    title('data')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    
    subplot(3,1,2)
    plot(PN_mat_plot(:,user),'linewidth',3)
    title('secuencia pseudo aleatoria')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    
    subplot(3,1,3)
    plot(signal_plot(:,user),'linewidth',3)
    title('senial codificada')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    title(strcat('Usuario ', user))
end
%% Combinacion de seniales

transmittesr_signal = sum(signal,2);
transmitter_signal_plot = sum(signal_plot,2);

figure
subplot(3,1,1)
plot(signal_plot(:,1),'linewidth',3)
title('senial a codificada user 1')
% configs grafico
set(gca,'XTick',0:n_PN*100:L);
set(gca,'XTickLabel',0:n_data);

subplot(3,1,2)
plot(signal_plot(:,2),'linewidth',3)
title('senial a codificada user 2')
% configs grafico
set(gca,'XTick',0:n_PN*100:L);
set(gca,'XTickLabel',0:n_data);

subplot(3,1,3)
plot(transmitter_signal_plot,'linewidth',3)
title('senial atransmitir')
% configs grafico
set(gca,'XTick',0:n_PN*100:L);
set(gca,'XTickLabel',0:n_data);
%%
% espectros
f_data = -pi:2*pi/length(data):pi-2*pi/length(data);
f_signal = -pi:2*pi/length(signal):pi-2*pi/length(signal);
figure
subplot(3,1,1)
stem(f_data,abs(fftshift(fft(data(:,1))))/length(data))
xlim([-pi pi])
subplot(3,1,2)
stem(f_signal,abs(fftshift(fft(signal(:,1))))/length(signal))
xlim([-pi pi])
subplot(3,1,3)
stem(f_signal,abs(fftshift(fft(signal(:,2))))/length(signal))
xlim([-pi pi])
%% Decodificacion
% 
for user = 1:n
    
    decoded_signal(:,user) = (reshape(transmittesr_signal,[n_PN n_data])'*PN(:,user));
    recovered_signal(decoded_signal(:,user) > 0) = 1;
    recovered_signal(decoded_signal(:,user) <= 0) = 0;
    
    
    %plots
    decoded_signal_plot = repelem(decoded_signal(:,user),500,1);
    recovered_signal_plot = repelem(recovered_signal',500,1);
    
    figure
    subplot(4,1,1)
    plot(transmitter_signal_plot,'linewidth',3)
    title('senial recibida')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    
    subplot(4,1,2)
    plot(PN_mat_plot(:,user),'linewidth',3)
    title('secuencia pseudo aleatoria')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    
    subplot(4,1,3)
    plot(recovered_signal_plot,'linewidth',3)
    title('senial decodificada')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
    
    subplot(4,1,4)
    plot(data_plot(:,user),'linewidth',3)
    title('data original')
    % configs grafico
    set(gca,'XTick',0:n_PN*100:L);
    set(gca,'XTickLabel',0:n_data);
end
