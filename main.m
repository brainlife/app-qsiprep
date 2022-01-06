function main()

% Add submodules (HCP systems)
if ~isdeployed
    addpath(genpath(pwd))
end

% load config.json
config = loadjson('config.json');

%% Flip the bvecs on x axis

%load bvecs
bvecs = dlmread(config.bvecs_out);

if ~(size(bvecs,1) == 3), bvecs = bvecs'; end
bvecs(1,:) = -bvecs(1,:);

dlmwrite('dwi.bvecs',bvecs,'delimiter',' ');

end
