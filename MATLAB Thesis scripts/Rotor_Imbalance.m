%This code is to generate statistics of different load channels for
%different levels of simulated rotor imbalance. 

%Terminology is as usual - MXYZ means Mass imbalance level X in blade 1, Y
%in balde 2, Z in blade 3. PXYZ means Pitch imbalance is level X in blade
%1, Y in blade 2, Z in blade 3.

clear
clc
rho = 1.225;
R = 178/2;
A = pi*R^2;
Wsp.Vo = [4;6;8;10;12;14;16;18;20;22;24];
%% If the results file has already been generated, this section will just load the results file and add some extra necessary columns.
%If the results file has not been generatedm this section cannot be run and
%the below sections need to be run to generate the results table.

load('Rotor_Imb_Results.mat')
ResultTable.sinc_NAcx = ResultTable.P1_NAcx./24000;
ResultTable.cosc_NAcx = ResultTable.P1_NAcx./24000;
ResultTable.sinc_NAcx = ResultTable.P1_NAcx./24000;
ResultTable.cosc_NAcy = ResultTable.P1_NAcx./24000;
%% Input options to generate a new results (fault simulations) table 'Rotor_Imb_results'.
%If it has already been generated, it can be loaded in the previous section and this section can be skipped
% Results from the '.stat' binary files  from the simulations will be grouped and stored in this file. 
%Results of a single binary file can be read using the script 'readstatfile.m'

 MLevel = {'M000';'M100';'M200';'M300';'M400';'M500'};
P1Level = {'P000';'P100';'P200';'P300';'P400';'P500';'P0_500';'P1_500'};
P2Level = {'P010';'P030'};
MValues = [0 0.5 2 4 5.5 6.8];
P1Values = [0 1 3 5 -1 -3 0.5 1.5];
P2Values = [1 5];
for M = 1:length(MLevel)
    ResultTable.MassImb(strcmp(ResultTable.MLevel,MLevel{M}))=MValues(M);
end
for P1 = 1:length(P1Level)
    ResultTable.PitchImb1(strcmp(ResultTable.PLevel,P1Level{P1}))=P1Values(P1);
end
for P2 = 1:length(P2Level)
    ResultTable.PitchImb2(strcmp(ResultTable.PLevel,P2Level{P2}))=P2Values(P2);
end
TSLevels = {'T1_S1';'T1_S2';'T2_S1';'T2_S2'};
TSValues = {'TI=0.12,S=0.2';'TI=0.12,S=0.1';'TI=0.12,S=0.2';'TI=0.12,S=0.1'};
ShearValues = [0.2 0.1 0.2 0.1];
% MLevel = {'M000';'M100';'M200';'M300';'M400';'M500'};
% PLevel = {'P000';'P100';'P200';'P300';'P400';'P500';'P010';'P030';'P050';};
MLevel = {'M100'};
PLevel = {'P030'};

j=0;
ResultTable1 = [];
for TS = 1:length(TSLevels)
    z=[];
    for M = 1:length(MLevel)
        for P = 1:length(PLevel)
            MPLevel = strcat(MLevel{M},PLevel{P});
            res_path=[];
            %if sum(strcmp(MPLevel,ResultTable.MPLevel))>0
                if strcmp(MPLevel,'M000P000')
                    res_path = ['C:\Master\Thesis\No_faults\HAWC2\' TSLevels{TS} '\' 'res\'];
                else
                    res_path = ['C:\Master\Thesis\Rotor Imbalance\HAWC2\' TSLevels{TS} '\' MPLevel '\res\' ];
                end
            %end
                if exist(res_path)==7
                    cd(res_path);
                    files = dir ('*.stat');
                    y=[];
                    for i=1:length(files)
                      if strcmp(MPLevel,'M000P000')  
                        a = strcat(files(i).name(09),files(i).name(10));
                      elseif strcmp(MPLevel,'M000P0_500') || strcmp(MPLevel,'M000P1_500')
                        a = strcat(files(i).name(15),files(i).name(16)); 
                      else
                        a = strcat(files(i).name(13),files(i).name(14));
                      end
                        V(i) = str2num(a);
                        files(i).Vo = V(i);
                    end

                    for i=1:length(Wsp.Vo)
                        ind = find([files.Vo]==Wsp.Vo(i));
                        for k = ind
                            j=j+1;
                            if strcmp(MPLevel,'M000P000')
                                x=readstatfile([res_path files(k).name],1,'Rotor_Imb_Vars.xlsx');
                            else
                                x=readstatfile1([res_path files(k).name],1,'Rotor_Imb_Vars.xlsx');
                            end
                            x.Vo = V(k)*ones(size(x,1),1);
                            x.MLevel = MLevel(M);
                            x.PLevel = PLevel(P);
                            x.TSLevel = TSLevels(TS);
                            x.Filename = string(x{1,1});
                            y=[y;x];
                        end
                   end
                z=[z;y];
            end
        end
    end
    ResultTable1 = [ResultTable1;z];
end
ResultTable1.MPLevel = strcat(ResultTable1.MLevel,ResultTable1.PLevel);
%% get the No_fault table - M000P000
ResultTable1=[];
for TS = 1:length(TSLevels)
    z=[];
    res_path = ['C:\Master\Thesis\No_faults\HAWC2\' TSLevels{TS} '\' 'res\'];   % path to HAWC2 (current folder)
    % go to htc folder, get file names and return
    if exist(res_path) == 7
        cd(res_path);
        files = dir ('*.stat');
        Wsp.string = ['04';'06';'08';'10';'12';'14';'16';'18';'20';'22';'24'];
        Wsp.Vo = [4;6;8;10;12;14;16;18;20;22;24];
        y=[];
        for i=1:length(files)
            a = strcat(files(i).name(09),files(i).name(10));
            V(i) = str2num(a);
            files(i).Vo = V(i);
        end
        
        for i=1:length(Wsp.Vo)
            ind = find([files.Vo]==Wsp.Vo(i));
            for k = ind
                j=j+1;
                x=readstatfile([res_path files(k).name],1,'Rotor_Imb_Vars.xlsx');
                x.Vo = V(k)*ones(size(x,1),1);
                x.MLevel = {'M000'};
                x.PLevel = {'P000'};
                x.TSLevel = TSLevels(TS);
                x.Filename = string(x{1,1});
                y=[y;x];
            end
        end
        z=[z;y];
    end
    ResultTable1 = [ResultTable1;z];
    ResultTable1.MLevel = string(ResultTable1.MLevel);
    ResultTable1.PLevel = string(ResultTable1.PLevel);
    ResultTable1.MPLevel = strcat(ResultTable1.MLevel,ResultTable1.PLevel);
end
%% Look at signal Mean Values for diff levels
MPneeded = {'M000P000';'M000P100';'M000P300';'M100P000';'M500P000';'M100P300';'M500P300'};
sigs = {'MxTB_Mean';'MyTB_Mean';'MzTB_Mean';'MxYB_Mean';'MyYB_Mean';'MzYB_Mean';'MxBR1_Mean';'MyBR1_Mean';'MzBR1_Mean';'MxBR2_Mean';'MyBR2_Mean';'MzBR2_Mean';'MxBR3_Mean';'MyBR3_Mean';'MzBR3_Mean'};
for i = 1:length(sigs)
    figure()
    for M = 1:length(MPneeded)
        Temp = ResultTable(strcmp(ResultTable.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Wind Speed [m/s]')
    ylabel(sigs{i})
    title(sigs{i})
    lgd=legend(MPneeded);
    lgd.Location = 'Best';
end
%% Only pitch imbalance - all levels in a graph
%sigs = {'MxTB_Mean';'MyTB_Mean';'MzTB_Mean';'MxYB_Mean';'MyYB_Mean';'MzYB_Mean';'MxBR1_Mean';'MyBR1_Mean';'MzBR1_Mean';'MxBR2_Mean';'MyBR2_Mean';'MzBR2_Mean';'MxBR3_Mean';'MyBR3_Mean';'MzBR3_Mean'};
channels = {'MxTB';'MyTB';'MzTB';'MxYB';'MyYB';'MzYB'};
Temp1 = ResultTable(strcmp(ResultTable.MLevel,'M000'),:);
stat = 'Max';
sigs = strcat(channels, '_',stat); 
LegendP = unique(Temp1.PitchImb1);
for i = 1:length(sigs)
    figure()
    MPneeded = unique(Temp1.MPLevel);
    for M = 1:length(MPneeded)
        Temp = Temp1(strcmp(Temp1.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('V_o [m/s]')
    ylabel([channels{i} ' ' stat ' [kNm]'])
    %title(sigs{i})
    lgd=legend(strcat(num2str(LegendP),'^o','Imb. B1'));
    lgd.Location = 'Best';
    savepath = 'C:\Master\Thesis\Rotor Imbalance\';
    saveas(gcf,[savepath 'PitchImb' stat sigs{i} ],'epsc')
end
%% Only mass imbalance - all levels in a graph
%sigs = {'MxTB_Mean';'MyTB_Mean';'MzTB_Mean';'MxYB_Mean';'MyYB_Mean';'MzYB_Mean';'MxBR1_Mean';'MyBR1_Mean';'MzBR1_Mean';'MxBR2_Mean';'MyBR2_Mean';'MzBR2_Mean';'MxBR3_Mean';'MyBR3_Mean';'MzBR3_Mean'};
sigs = {'MyBR1_Std';'MyBR2_Std';'MyBR3_Std';'MyBR1_Max';'MyBR2_Max';'MyBR3_Max'};
Temp1 = ResultTable(strcmp(ResultTable.PLevel,'P000'),:);
for i = 1:length(sigs)
    figure()
    MPneeded = unique(Temp1.MPLevel);
    for M = 1:length(MPneeded)
        Temp = Temp1(strcmp(Temp1.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Wind Speed [m/s]')
    ylabel(sigs{i})
    title(sigs{i})
    lgd=legend(MPneeded);
    lgd.Location = 'Best';
end
%% Only pitch imbalance - all levels in a graph - tower top and bottom
sigs = {'MxTB_Mean';'MyTB_Mean';'MzTB_Mean';'MxYB_Mean';'MyYB_Mean';'MzYB_Mean';'MxBR1_Mean';'MyBR1_Mean';'MzBR1_Mean';'MxBR2_Mean';'MyBR2_Mean';'MzBR2_Mean';'MxBR3_Mean';'MyBR3_Mean';'MzBR3_Mean'};
Temp1 = ResultTable(strcmp(ResultTable.MLevel,'M000'),:);
for i = 1:length(sigs)
    figure()
    MPneeded = unique(Temp1.MPLevel);
    for M = 1:length(MPneeded)
        Temp = Temp1(strcmp(Temp1.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Wind Speed [m/s]')
    ylabel(sigs{i})
    title(sigs{i})
    lgd=legend(MPneeded);
    lgd.Location = 'Best';
end
%% Only mass imbalance - std. all levels in a graph - tower top and bottom
sigs = {'MxTB_Std';'MyTB_Std';'MzTB_Std';'MxYB_Std';'MyYB_Std';'MzYB_Std';'MxBR1_Std';'MyBR1_Std';'MzBR1_Std';'MxBR2_Std';'MyBR2_Std';'MzBR2_Std';'MxBR3_Std';'MyBR3_Std';'MzBR3_Std'};
Temp1 = ResultTable(strcmp(ResultTable.PLevel,'P000'),:);
for i = 1:length(sigs)
    figure()
    MPneeded = unique(Temp1.MPLevel);
    for M = 1:length(MPneeded)
        Temp = Temp1(strcmp(Temp1.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Wind Speed [m/s]')
    ylabel(sigs{i})
    title(sigs{i})
    lgd=legend(MPneeded);
    lgd.Location = 'Best';
end
%% Only pitch imbalance - std. all levels in a graph - blade root
channels = {'MxBR1';'MxBR2';'MxBR3'};
Temp1 = ResultTable(strcmp(ResultTable.MLevel,'M000'),:);
%Temp1 = ResultTable(ismember(ResultTable.PLevel,{'P010','P030'}),:);
stat = 'Mean';
sigs = strcat(channels, '_',stat); 
LegendP = unique(Temp1.PitchImb1);
for i = 1:length(sigs)
    figure()
    MPneeded = unique(Temp1.MPLevel);
    for M = 1:length(MPneeded)
        Temp = Temp1(strcmp(Temp1.MPLevel,MPneeded{M}),:);
        DataTable = grpstats(Temp,'Vo','mean','DataVars',{'Vo',sigs{i}});
        var = ['mean_' sigs{i}];
        plot(DataTable.mean_Vo,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('V_o [m/s]')
    ylabel([channels{i} ' ' stat ' [kNm]'])
    %title(sigs{i})
    lgd=legend(strcat(num2str(LegendP),'^o','Imb. B1'));
    lgd.Location = 'Best';
    savepath = 'C:\Master\Thesis\Rotor Imbalance\';
    saveas(gcf,[savepath 'PitchImb' stat sigs{i} ],'epsc')
end
%% plot by signal vs fault intensity - mass imbalance
%Wsp.Vo = [4;6;8;10;12;14;16];
%sigs = {'MxTB_Std';'MyTB_Std';'MzTB_Std';'MxYB_Std';'MyYB_Std';'MzYB_Std';'MxBR1_Std';'MyBR1_Std';'MzBR1_Std';'MxBR2_Std';'MyBR2_Std';'MzBR2_Std';'MxBR3_Std';'MyBR3_Std';'MzBR3_Std'};
%sigs={'MxYB_Std';'MyYB_Std';'MzYB_Std'};
channels={'P1_NAcx';'P1_NAcy'};
Temp1 = ResultTable(strcmp(ResultTable.PLevel,'P000'),:);
stat = 'Std';
sigs = strcat(channels, '_', stat);
for i = 1:length(sigs)
    figure()
    for j = 1:length(Wsp.Vo)
        Temp = Temp1(Temp1.Vo==Wsp.Vo(j),:);
        Temp = sortrows(Temp,'MassImb');
        DataTable = grpstats(Temp,'MLevel','mean','DataVars',{'Vo','MassImb','PitchImb1','PitchImb2',sigs{i}});
        var = [ 'mean' '_' sigs{i}];
        plot(DataTable.mean_MassImb,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Mass Imbalance (% of blade mass)')
    ylabel([channels{i} ' ' stat ' [kNm]'])
    title(sigs{i})
    lgd=legend(strcat(num2str(Wsp.Vo),' m/s'));
    lgd.Location = 'Best';

end

%% plot by signal vs fault intensity - pitch imbalance 1
Wsp.Vo = [4;6;8;10;12];
%sigs = {'MxTB_Std';'MyTB_Std';'MzTB_Std';'MxYB_Std';'MyYB_Std';'MzYB_Std';'MxBR1_Std';'MyBR1_Std';'MzBR1_Std';'MxBR2_Std';'MyBR2_Std';'MzBR2_Std';'MxBR3_Std';'MyBR3_Std';'MzBR3_Std'};
channels={'MxTB';'MyTB';'MzTB';'MxYB';'MyYB';'MzYB'};
stat = 'Mean';
sigs = strcat(channels,'_',stat);
Temp1 = ResultTable(strcmp(ResultTable.MLevel,'M000')&ResultTable.PitchImb2==0,:);
for i = 1:length(sigs)
    figure()
    for j = 1:length(Wsp.Vo)
        Temp = Temp1(Temp1.Vo==Wsp.Vo(j),:);
        Temp = sortrows(Temp,'PitchImb1');
        DataTable = grpstats(Temp,'PLevel','mean','DataVars',{'Vo','MassImb','PitchImb1','PitchImb2',sigs{i}});
        var = [ 'mean' '_' sigs{i}];
        plot(DataTable.mean_PitchImb1,DataTable.(var),'-o','LineWidth',1.25)
        hold on
    end
    grid on
    xlabel('Pitch Imbalance [deg]')
    ylabel([channels{i} ' ' stat ' [kNm]'])
    %title(sigs{i})
    lgd=legend(strcat(num2str(Wsp.Vo),' m/s'));
    lgd.Location = 'Best';
    savepath = 'C:\Master\Thesis\Rotor Imbalance\';
    saveas(gcf,[savepath 'PitchImb' stat sigs{i} ],'epsc')
end
