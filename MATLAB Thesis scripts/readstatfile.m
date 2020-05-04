%%
%filename should be with extension .stat
%returns a table with one column of headers and another one with the
%corresponding values
%OnlyFewVars - switch to read only specific variables for eg. power, pitch
%etc.
%OnlyFewVars - For now - mean, min, max of Pitch, Power and Torque

function x =readstatfile(filename,OnlyFewVars,varlistxls)
%read file contents into a cell array
fields_per_line = 697; %no. of columns of the standard .stat file
fmt = repmat('%s',1,fields_per_line);
fid = fopen(filename, 'rt');
filebycolumn = textscan(fid, fmt, 'Delimiter', ';');

%convert cell array to a struct 
if OnlyFewVars==0
    for i=1:length(filebycolumn)
        x(i).headers = filebycolumn{i}{1};
        x(i).values = filebycolumn{i}{2};
        if i>1
            x(i).values = str2double(x(i).values);
        end
    end 
end

if OnlyFewVars==1
        a=readtable(varlistxls);
        var = a{:,1};
        for i = 2:length(var)
            var{i} = [var{i} ' '];
        end
        Names = a{:,2};
%         var{1}='Ch 12 Aero rotor power Mean ';
%         var{2}= 'Ch 11 Aero rotor torque Mean ';
%         var{3}= 'Ch 4 pitch1 angle Mean '; 
%         var{4} = 'Ch 12 Aero rotor power Max ';
%         var{5} = 'Ch 11 Aero rotor torque Max ';
%         var{6} = 'Ch 4 pitch1 angle Max ';
%         var{7} = 'Ch 12 Aero rotor power Min ';
%         var{8} = 'Ch 11 Aero rotor torque Min ';
%         var{9} = 'Ch 4 pitch1 angle Min ';
%         var{10} = 'Filename';
    j=0;
    for i=1:length(filebycolumn)       
        if sum(strcmp(var,filebycolumn{i}{1})) %sum can be max 1
            j=j+1;
            x(j).headers = filebycolumn{i}{1};
            x(j).values = filebycolumn{i}{2};
            if i>1
                x(j).values = str2double(x(j).values);
            end
        end
    end
end
%convert struct to table because I like working with tables more :P
x=rows2vars(struct2table(x));  

%set modified variable names from first row as table headers and delete the first row
% for i=1:size(x,2)
%       if strcmp(x{1,i}{1},'headers')
%         x.Properties.VariableNames{i} ='headers';
%       elseif strcmp(x{1,i}{1},var{1})
%         x.Properties.VariableNames{i} ='Mean_Power'; 
%       elseif strcmp(x{1,i}{1},var{2})
%         x.Properties.VariableNames{i} ='Mean_Torque'; 
%       elseif strcmp(x{1,i}{1},var{3})
%         x.Properties.VariableNames{i} ='Mean_Pitch_B1';
%       elseif strcmp(x{1,i}{1},var{4})
%         x.Properties.VariableNames{i} ='Max_Power'; 
%       elseif strcmp(x{1,i}{1},var{5})
%         x.Properties.VariableNames{i} ='Max_Torque'; 
%       elseif strcmp(x{1,i}{1},var{6})
%         x.Properties.VariableNames{i} ='Max_Pitch_B1';
%       elseif strcmp(x{1,i}{1},var{7})
%         x.Properties.VariableNames{i} ='Min_Power'; 
%       elseif strcmp(x{1,i}{1},var{8})
%         x.Properties.VariableNames{i} ='Min_Torque'; 
%       elseif strcmp(x{1,i}{1},var{9})
%         x.Properties.VariableNames{i} ='Min_Pitch_B1';
%       elseif strcmp(x{1,i}{1},var{10})
%         x.Properties.VariableNames{i} ='Filename';
%       end
% end
%delete first row and first column, which is just a useless string
%'headers'
x(1,:) = [];
x(:,1) = [];
for i =1:size(x,2)
    x.Properties.VariableNames{i} = Names{i};
end
%why the hell are the values in x of type cells? Irritating! AAAARRRRRGHHHHHH!!!!
%convert values in x from cell to double
for i = 1:size(x,2)
   if iscell(x.(i))
      x.(i) = cell2mat(x.(i)); 
   end
end
x{1,1}=string(x{1,1});
%Create the column for seeds
% x.Seed = str2double(x.Filename(13:16));
%x.Seed = str2double(extractBetween(x.Filename,'_s','_t'));
%close file
fclose(fid);
end