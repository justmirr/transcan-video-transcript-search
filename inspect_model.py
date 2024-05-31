import torch
import os

model_path = 'tiny.en.pt'
model_data = torch.load(model_path)

state_dict = model_data['model_state_dict']

print("Model State Dictionary Contents:\n")
for key, value in state_dict.items():
    print(f"{key}: {value.size()}")

output_file = 'model_summary.txt'
with open(output_file, 'w') as f:
    f.write("Model State Dictionary Contents:\n\n")
    for key, value in state_dict.items():
        f.write(f"{key}: {value.size()}\n")
print(f"\nModel summary saved to {output_file}")

print("\nModel Summary:")
total_params = 0
for key, value in state_dict.items():
    num_params = value.numel()
    total_params += num_params
    print(f"{key}: {value.size()} (Parameters: {num_params})")

print(f"\nTotal Parameters: {total_params}")

output_dir = 'model_output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_model_path = os.path.join(output_dir, 'model_state_dict.pth')
torch.save(state_dict, output_model_path)
print(f"\nState dictionary saved to {output_model_path}")

model_dims = model_data['dims']
print("\nModel Dimensions:")
for dim_key, dim_value in model_dims.items():
    print(f"{dim_key}: {dim_value}")
