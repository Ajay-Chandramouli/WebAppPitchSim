%This function is to read .stat files produced by the HAWC2 simulations
%input filename should be with extension .stat
%returns a table with one column of headers and another one with the
%corresponding values
%OnlyFewVars - switch to read only specific variables for eg. power, pitch
%etc.
%OnlyFewVars - list available in excel file

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
        a=readtable(varlistxls); %excel file containing variables list to be read
        var = a{:,1};
        for i = 2:length(var)
            var{i} = [var{i} ' '];
        end
        Names = a{:,2};
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
%close file
fclose(fid);
end