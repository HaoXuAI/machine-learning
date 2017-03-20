function [ index ] = sampler( params )

val = rand(1);
for i = 1:length(params);
    if sum(params(1:i)) >= val
        index = i;
        break;
    end
end
end

